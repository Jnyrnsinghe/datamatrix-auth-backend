from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import LoginEvent, SessionToken, User
from app.notifications import send_login_notification
from app.schemas import (
    CreateUserRequest,
    LoginRequest,
    TokenResponse,
    TokenValidationRequest,
    TokenValidationResponse,
    UserResponse,
)
from app.security import create_access_token, decode_access_token, hash_password, verify_password

app = FastAPI(title=settings.app_name)


def ensure_utc_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def require_admin_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not settings.admin_api_key or x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin API key")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": settings.app_env}


@app.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == payload.username))
    request_ip = request.client.host if request.client else None

    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        db.add(
            LoginEvent(
                username=payload.username,
                success=False,
                machine_name=payload.machine_name,
                app_version=payload.app_version,
                ip_address=request_ip,
            )
        )
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token, expires_at = create_access_token(user.username)
    user.last_login_at = datetime.now(timezone.utc)
    db.add(
        SessionToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
        )
    )
    db.add(
        LoginEvent(
            username=user.username,
            success=True,
            machine_name=payload.machine_name,
            app_version=payload.app_version,
            ip_address=request_ip,
        )
    )
    db.commit()

    await send_login_notification(user.username, payload.machine_name, payload.app_version)

    return TokenResponse(
        access_token=token,
        expires_at=expires_at,
        offline_grace_days=settings.offline_grace_days,
        full_name=user.full_name,
    )


@app.post("/validate-token", response_model=TokenValidationResponse)
def validate_token(payload: TokenValidationRequest, db: Session = Depends(get_db)) -> TokenValidationResponse:
    try:
        token_payload = decode_access_token(payload.token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    username = token_payload.get("sub")
    session = db.scalar(select(SessionToken).where(SessionToken.token == payload.token))
    session_expires_at = ensure_utc_datetime(session.expires_at) if session else None

    if session is None or session_expires_at is None or session_expires_at < datetime.now(timezone.utc):
        return TokenValidationResponse(valid=False)

    return TokenValidationResponse(valid=True, username=username, expires_at=session_expires_at)


@app.post("/admin/create-user", response_model=UserResponse)
def create_user(
    payload: CreateUserRequest,
    _: None = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> UserResponse:
    existing_user = db.scalar(select(User).where(User.username == payload.username))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
    )
