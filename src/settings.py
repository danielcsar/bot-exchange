from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_TOKEN: str
    DATABASE_NAME: str
    DATABASE_URL: str
    NOTIFICATION_URL: str
    BOT_URL: str
    BOT_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")
