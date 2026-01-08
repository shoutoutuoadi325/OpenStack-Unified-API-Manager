"""Pydantic schemas shared by routers."""

from typing import Literal
from pydantic import BaseModel, Field


class ServerCreate(BaseModel):
    """Payload for provisioning a new server."""

    name: str
    image_id: str = Field(..., description="Glance image ID")
    flavor_id: str = Field(..., description="Nova flavor ID")
    network_id: str = Field(..., description="Neutron network ID to attach")
    key_name: str | None = Field(None, description="Existing Nova keypair name")
    security_groups: list[str] = Field(default_factory=list)
    user_data: str | None = Field(None, description="Base64 encoded cloud-init user-data")
    availability_zone: str | None = None


class ServerAction(BaseModel):
    """Action against an existing server."""

    action: Literal["start", "stop", "reboot", "pause", "unpause", "suspend", "resume"]
    hard: bool = Field(False, description="Use hard reboot when action is reboot")


class VolumeCreate(BaseModel):
    """Payload for provisioning a Cinder volume."""

    name: str | None = None
    size: int = Field(..., description="Size in GiB")
    description: str | None = None
    snapshot_id: str | None = None
    volume_type: str | None = None


class ContainerCreate(BaseModel):
    """Payload for creating a Swift container."""

    name: str
    metadata: dict[str, str] | None = None


class ApiMessage(BaseModel):
    """Simple message envelope."""

    message: str

