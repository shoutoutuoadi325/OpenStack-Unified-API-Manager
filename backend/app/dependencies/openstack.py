"""OpenStack SDK dependency wiring."""

from functools import lru_cache
from fastapi import Depends
from openstack import connection
from app.config import Settings, get_settings


@lru_cache
def _connection_cache(
    auth_url: str,
    username: str,
    password: str,
    project_name: str,
    user_domain_name: str,
    project_domain_name: str,
    region_name: str,
    interface: str,
    verify: bool | str,
    request_timeout: int,
) -> connection.Connection:
    """Cache the SDK connection per unique credential set."""
    return connection.Connection(
        auth_url=auth_url,
        username=username,
        password=password,
        project_name=project_name,
        user_domain_name=user_domain_name,
        project_domain_name=project_domain_name,
        region_name=region_name,
        interface=interface,
        verify=verify,
        timeout=request_timeout,
    )


def get_openstack_conn(settings: Settings = Depends(get_settings)) -> connection.Connection:
    """Provide a cached OpenStack connection for FastAPI dependencies."""
    return _connection_cache(
        settings.auth_url,
        settings.username,
        settings.password,
        settings.project_name,
        settings.user_domain_name,
        settings.project_domain_name,
        settings.region_name,
        settings.interface,
        settings.verify,
        settings.request_timeout,
    )

