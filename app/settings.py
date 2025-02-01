from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core settings
    cors_origins: str = "*"
    secret_key: str = "BMHPs/ozOP4sHN9rzvNCiu7rtUHZ2d0H0NFm5+dj5n4="
    access_token_expire_minutes: int = 120

    # Database variables (Overwrite in .env file)
    db_user: str = "postgres"
    db_password: str = "159357"
    db_port: int = 5432
    db_name: str = "bron_db"
    db_address: str = "localhost"

    # Test database variables
    test_db_user: str = "postgres"
    test_db_password: str = "159357"
    test_db_port: int = 5432
    test_db_name: str = "bron_test_db"
    test_db_address: str = "localhost"

    # Metadata variables
    title: str = "My FastAPI App"
    description: str = "This is a FastAPI application."
    version: str = "v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    # class Config:
    #     env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
