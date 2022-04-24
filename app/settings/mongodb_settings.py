from functools import lru_cache

from pydantic import BaseSettings


class MongodbSettings(BaseSettings):

    mongodb_url: str


@lru_cache()
def get_mongodb_settings():
    return MongodbSettings()
