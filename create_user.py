import typer
from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password

cli = typer.Typer()


@cli.command()
def main(username: str, password: str, full_name: str = "") -> None:
    db = SessionLocal()
    try:
        existing_user = db.scalar(select(User).where(User.username == username))
        if existing_user:
            typer.echo(f"User '{username}' already exists.")
            raise typer.Exit(code=1)

        user = User(
            username=username,
            password_hash=hash_password(password),
            full_name=full_name or None,
            is_active=True,
        )
        db.add(user)
        db.commit()
        typer.echo(f"Created user '{username}'.")
    finally:
        db.close()


if __name__ == "__main__":
    cli()
