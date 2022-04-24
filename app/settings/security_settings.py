from functools import lru_cache

from pydantic import BaseSettings


class SecuritySettings(BaseSettings):

    secret_key: str
    secure_keyword: str


@lru_cache()
def get_security_settings():
    return SecuritySettings()
