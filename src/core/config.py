from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_PLAYER_URL: str
    DB_NPC_URL: str
    TELEGRAM_BOT_TOKEN: str


settings = Settings()
