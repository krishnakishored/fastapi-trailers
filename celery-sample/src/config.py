import logging
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)  # with increased verbosity
# load_dotenv()
class CelerySettings(BaseSettings):
    """
    Celery settings for worker threads
    """

    CELERY_BROKER_URL: str = "redis://db_redis_redis-server:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://db_redis_redis-server:6379/0"
    FLOWER_PORT: int = 5556


class Settings(CelerySettings):
    HOST: str = "0.0.0.0"
    TASKER_PORT: int = 40008

    APP_NAME: str = "TASKER"
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


# settings = Settings() #  default instance is not created if 'Depends' is used
