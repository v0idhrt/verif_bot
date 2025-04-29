# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    discord_token: str
    guild_id: int
    male_role_id: int
    female_role_id: int
    unverified_role_id: int
    support_role_id: int
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
