"""Block storage (Cinder) operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn
from app.schemas import ApiMessage, VolumeCreate

router = APIRouter(prefix="/block-storage", tags=["block-storage"])


def _volume_view(volume: object) -> dict:
    return {
        "id": volume.id,
        "name": volume.name,
        "status": volume.status,
        "size": getattr(volume, "size", None),
        "description": getattr(volume, "description", None),
        "bootable": getattr(volume, "is_bootable", getattr(volume, "bootable", False)),
        "attachments": getattr(volume, "attachments", []),
        "created_at": getattr(volume, "created_at", None),
    }


@router.get("/volumes")
def list_volumes(conn=Depends(get_openstack_conn)):
    """List Cinder volumes."""
    try:
        return [_volume_view(vol) for vol in conn.block_storage.volumes(details=True)]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/volumes/{volume_id}")
def get_volume(volume_id: str, conn=Depends(get_openstack_conn)):
    """Fetch a volume."""
    try:
        volume = conn.block_storage.get_volume(volume_id)
        if not volume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found")
        return _volume_view(volume)
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.post("/volumes", status_code=status.HTTP_202_ACCEPTED)
def create_volume(payload: VolumeCreate, conn=Depends(get_openstack_conn)):
    """Provision a volume."""
    try:
        volume = conn.block_storage.create_volume(
            name=payload.name,
            size=payload.size,
            description=payload.description,
            snapshot_id=payload.snapshot_id,
            volume_type=payload.volume_type,
        )
        return _volume_view(volume)
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.delete("/volumes/{volume_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ApiMessage)
def delete_volume(volume_id: str, conn=Depends(get_openstack_conn)):
    """Delete a volume."""
    try:
        conn.block_storage.delete_volume(volume_id, ignore_missing=False)
        return ApiMessage(message=f"Deletion requested for volume {volume_id}")
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

