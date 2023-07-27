import logging
import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

# from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(verbose=True)  # with increased verbosity


class Settings(BaseSettings):
    APP_NAME: str = "quester"
    APP_VERSION: str = os.environ.get("APP_VERSION", "0.9")
    APP_DESCRIPTION: str = os.environ.get(
        "APP_DESCRIPTION",
        "A backend app that provides the search and filter functions"
        + "and json logging enabled",
    )
    HOST: str = "0.0.0.0"
    PORT: int = 7600
    DEBUG_MODE: bool = False  # TODO: reading bool from env
    # NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, CRITICAL=50
    # in general set DEBUG for dev, WARN for production(least longing)
    LOG_LEVEL: int = logging.INFO  # info level logs req-resp json
    GUNICORN_WORKERS: int = 1  # A +ve integer in the 2-4 x $(NUM_CORES) range.
    # Workers silent for more than this many seconds are killed and restarted.
    GUNICORN_TIMEOUT: int = 120

    SOLR_BASE_URL: str = "http://localhost:8983"

    class Config:
        env_file = ".env"

    # TODO: move to pydantic_settings
    # model_config: ConfigDict = SettingsConfigDict(
    #     env_file=".env", extra="ignore"
    # )


# @lru_cache() modifies the function it decorates to return the same value that
# was returned the first time, instead of executing the code every time.
@lru_cache()
def get_settings():
    return Settings()


# # settings = Settings() #  default instance is not created if 'Depends' is used
