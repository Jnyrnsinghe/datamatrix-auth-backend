from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "DataMatrix Auth Backend"
    app_env: str = "development"
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_days: int = 7
    offline_grace_days: int = 3
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    admin_api_key: str = ""


settings = Settings()
