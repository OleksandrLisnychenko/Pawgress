import os
from functools import lru_cache


class Settings:
    database_url: str = os.environ.get("PAWGRESS_DATABASE_URL", "sqlite:///./pawgress.db")


@lru_cache
def get_settings() -> Settings:
    return Settings()
