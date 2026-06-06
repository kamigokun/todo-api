from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    All app configuration is loaded from the .env file.
    Pydantic reads the .env file and maps each variable
    to the fields defined below automatically.
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  # tells pydantic where to look


# This creates ONE instance of Settings that the whole app shares.
# Any file that needs config just imports this `settings` object.
settings = Settings()