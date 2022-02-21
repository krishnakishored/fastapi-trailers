import logging
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)  # with increased verbosity
# load_dotenv()
class DBSettings(BaseSettings):
    """
    POSTGRES params
    """

    PG_DBHOST: str = "POSTGRES_DBHOST"
    PG_DBPORT: str = "5432"
    PG_DBNAME: str = "POSTGRES_DBNAME"
    PG_DBUSER: str = "POSTGRES_DBUSER"
    PG_DBPASS: str = "POSTGRES_DBNAME"


class Settings(
    DBSettings,
):
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    APP_NAME: str = "FastAPI-CRUD"
    DEBUG_MODE: bool = False
    # NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, CRITICAL=50
    LOG_LEVEL: int = logging.INFO  # info level logs req-resp json
    # in general set DEBUG for dev, WARN for production(least longing)

    class Config:
        # ToDo: Read the urls from environment
        env_file = ".env"  # override the defaults
        # env_file_encoding = 'utf-8'


# @lru_cache() modifies the function it decorates to return the same value that was returned the first time, instead of executing the code every time
@lru_cache()
def get_settings():
    return Settings()
