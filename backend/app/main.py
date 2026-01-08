"""FastAPI entrypoint for the Unified OpenStack API Manager."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    block_storage,
    compute,
    health,
    identity,
    image,
    network,
    object_storage,
)

app = FastAPI(
    title="OpenStack Unified API Manager",
    version="0.1.0",
    description="Single-console API to manage Nova, Keystone, Glance, Neutron, Swift, and Cinder.",
)

# Allow local dev origins; tighten for production deployments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(identity.router)
app.include_router(compute.router)
app.include_router(image.router)
app.include_router(network.router)
app.include_router(object_storage.router)
app.include_router(block_storage.router)


@app.get("/")
def root():
    """Basic landing endpoint."""
    return {"service": "openstack-unified-api-manager", "endpoints": ["/health", "/identity", "/compute", "/images", "/network", "/object-storage", "/block-storage"]}

