"""Image (Glance) operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn

router = APIRouter(prefix="/images", tags=["images"])


def _image_view(image: object) -> dict:
    return {
        "id": image.id,
        "name": image.name,
        "status": image.status,
        "visibility": getattr(image, "visibility", None),
        "size": getattr(image, "size", None),
        "disk_format": getattr(image, "disk_format", None),
        "container_format": getattr(image, "container_format", None),
        "min_disk": getattr(image, "min_disk", None),
        "min_ram": getattr(image, "min_ram", None),
        "created_at": getattr(image, "created_at", None),
    }


@router.get("")
def list_images(
    visibility: str | None = Query(None, description="Filter by visibility (public, private, shared)"),
    conn=Depends(get_openstack_conn),
):
    """List images."""
    try:
        return [_image_view(img) for img in conn.image.images(visibility=visibility)]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/{image_id}")
def get_image(image_id: str, conn=Depends(get_openstack_conn)):
    """Fetch an image."""
    try:
        image = conn.image.get_image(image_id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        return _image_view(image)
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

