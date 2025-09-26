from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Local Skill-Sharing Event Platform"
    secret_key: str
    access_token_expire_minutes: int = 60 * 24
    database_url: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
