from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GITHUB_TOKEN: str | None = None  # optional GitHub token (from .env file)

    class Config:
        env_file = ".env"  # load environment variables from .env

settings = Settings()
