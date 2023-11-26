import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool
    environment: str
    load_models: bool
    redis_host: str
    static_dir: str

    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_host: str
    postgres_port: str


settings = Settings()
