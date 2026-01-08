"""Object storage (Swift) operations."""

from fastapi import APIRouter, Depends, HTTPException
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn
from app.schemas import ApiMessage, ContainerCreate

router = APIRouter(prefix="/object-storage", tags=["object-storage"])


def _container_view(container: object) -> dict:
    return {
        "name": container.name,
        "count": getattr(container, "count", None),
        "bytes": getattr(container, "bytes", None),
        "timestamp": getattr(container, "timestamp", None),
    }


def _object_view(obj: object) -> dict:
    return {
        "name": obj.name,
        "content_type": getattr(obj, "content_type", None),
        "bytes": getattr(obj, "bytes", None),
        "last_modified": getattr(obj, "last_modified", None),
        "hash": getattr(obj, "hash", None),
    }


@router.get("/containers")
def list_containers(conn=Depends(get_openstack_conn)):
    """List Swift containers."""
    try:
        return [_container_view(container) for container in conn.object_store.containers()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.post("/containers", response_model=ApiMessage, status_code=201)
def create_container(payload: ContainerCreate, conn=Depends(get_openstack_conn)):
    """Create a Swift container."""
    try:
        conn.object_store.create_container(
            name=payload.name,
            metadata=payload.metadata or {},
        )
        return ApiMessage(message=f"Container {payload.name} created")
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/containers/{container_name}/objects")
def list_objects(container_name: str, conn=Depends(get_openstack_conn)):
    """List objects within a container."""
    try:
        return [_object_view(obj) for obj in conn.object_store.objects(container=container_name)]
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=404, detail="Container not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

