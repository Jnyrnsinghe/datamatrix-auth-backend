import httpx

from app.config import settings


async def send_login_notification(username: str, machine_name: str | None, app_version: str | None) -> None:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return

    message = (
        "New DataMatrix app login\n"
        f"User: {username}\n"
        f"Machine: {machine_name or 'unknown'}\n"
        f"Version: {app_version or 'unknown'}"
    )

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {"chat_id": settings.telegram_chat_id, "text": message}

    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json=payload)
