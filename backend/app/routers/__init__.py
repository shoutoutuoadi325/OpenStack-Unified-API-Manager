"""Router exports."""

from app.routers import block_storage, compute, health, identity, image, network, object_storage

__all__ = [
    "block_storage",
    "compute",
    "health",
    "identity",
    "image",
    "network",
    "object_storage",
]

