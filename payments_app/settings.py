from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    database_url: str = "postgresql://db_user:db_password@localhost:5432/payments_db"

    class Config:
        env_file = ".env"


settings = AppSettings()
