from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ToDo API"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./todo.db"

    jwt_secret_key: str = "anthony_lanson"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()