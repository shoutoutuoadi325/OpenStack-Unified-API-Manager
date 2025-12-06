"""Configuration helpers for the FastAPI app."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven OpenStack and service configuration."""

    auth_url: str
    username: str
    password: str
    project_name: str
    user_domain_name: str = "Default"
    project_domain_name: str = "Default"
    region_name: str = "RegionOne"
    interface: str = "public"
    verify: bool | str = True  # Can be a CA bundle path
    request_timeout: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_prefix="OS_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings loaded from environment."""
    return Settings()

