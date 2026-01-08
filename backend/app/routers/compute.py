"""Compute (Nova) operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn
from app.schemas import ApiMessage, ServerAction, ServerCreate

router = APIRouter(prefix="/compute", tags=["compute"])


def _serialize_server(server: object) -> dict:
    """Return a trimmed server representation safe for the API."""
    networks = server.addresses or {}
    image_id = getattr(server.image, "id", None) if getattr(server, "image", None) else None
    flavor_id = getattr(server.flavor, "id", None) if getattr(server, "flavor", None) else None
    return {
        "id": server.id,
        "name": server.name,
        "status": server.status,
        "addresses": networks,
        "image_id": image_id,
        "flavor_id": flavor_id,
        "created_at": getattr(server, "created_at", None),
        "updated_at": getattr(server, "updated_at", None),
        "metadata": getattr(server, "metadata", {}),
    }


@router.get("/servers")
def list_servers(
    all_projects: bool = Query(False, description="List servers across projects (admin only)"),
    conn=Depends(get_openstack_conn),
):
    """List servers with lightweight details."""
    try:
        servers = conn.compute.servers(details=True, all_projects=all_projects)
        return [_serialize_server(srv) for srv in servers]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/flavors")
def list_flavors(conn=Depends(get_openstack_conn)):
    """List available compute flavors."""
    try:
        return [
            {
                "id": flavor.id,
                "name": flavor.name,
                "vcpus": getattr(flavor, "vcpus", None),
                "ram_mb": getattr(flavor, "ram", None),
                "disk_gb": getattr(flavor, "disk", None),
            }
            for flavor in conn.compute.flavors(details=True)
        ]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/servers/{server_id}")
def get_server(server_id: str, conn=Depends(get_openstack_conn)):
    """Fetch a single server."""
    try:
        server = conn.compute.get_server(server_id)
        if not server:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
        return _serialize_server(server)
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.post("/servers", status_code=status.HTTP_202_ACCEPTED)
def create_server(payload: ServerCreate, conn=Depends(get_openstack_conn)):
    """Provision a new server."""
    try:
        server = conn.compute.create_server(
            name=payload.name,
            image_id=payload.image_id,
            flavor_id=payload.flavor_id,
            networks=[{"uuid": payload.network_id}],
            key_name=payload.key_name,
            security_groups=[{"name": sg} for sg in payload.security_groups],
            user_data=payload.user_data,
            availability_zone=payload.availability_zone,
        )
        conn.compute.wait_for_server(server, status="ACTIVE")
        return _serialize_server(server)
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.post("/servers/{server_id}/actions", response_model=ApiMessage)
def mutate_server(server_id: str, action: ServerAction, conn=Depends(get_openstack_conn)):
    """Execute a lifecycle action against a server."""
    try:
        action_map = {
            "start": conn.compute.start_server,
            "stop": conn.compute.stop_server,
            "reboot": lambda sid: conn.compute.reboot_server(sid, reboot_type="HARD" if action.hard else "SOFT"),
            "pause": conn.compute.pause_server,
            "unpause": conn.compute.unpause_server,
            "suspend": conn.compute.suspend_server,
            "resume": conn.compute.resume_server,
        }
        handler = action_map[action.action]
        handler(server_id)
        return ApiMessage(message=f"{action.action} requested for server {server_id}")
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.delete("/servers/{server_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ApiMessage)
def delete_server(server_id: str, conn=Depends(get_openstack_conn)):
    """Delete a server."""
    try:
        conn.compute.delete_server(server_id, ignore_missing=False)
        return ApiMessage(message=f"Deletion requested for server {server_id}")
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err
