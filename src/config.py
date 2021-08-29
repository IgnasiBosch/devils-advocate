from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    default_secs_per_round: int = 90
    session_token_algorithm: str = "HS256"
    session_token_key: str = (
        "ae1cbe817d9f0792b569a7504a07deb42d09dab609c92b949972cad1787c9b2c"
    )
    session_token_exp_time: int = 180
    database_uri = "sqlite:///database.db"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
