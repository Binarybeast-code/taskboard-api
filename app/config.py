from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./taskboard.db" #sqlite database file will be created in the current directory
    app_name: str = "Task Board API"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

