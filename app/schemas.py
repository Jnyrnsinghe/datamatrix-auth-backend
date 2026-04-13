from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str
    machine_name: str | None = None
    app_version: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    offline_grace_days: int
    full_name: str | None = None


class TokenValidationResponse(BaseModel):
    valid: bool
    username: str | None = None
    expires_at: datetime | None = None


class TokenValidationRequest(BaseModel):
    token: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    full_name: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str | None = None
    is_active: bool
    created_at: datetime
