"""Identity (Keystone) operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn

router = APIRouter(prefix="/identity", tags=["identity"])


def _project_view(project: object) -> dict:
    return {
        "id": project.id,
        "name": project.name,
        "description": getattr(project, "description", ""),
        "domain_id": getattr(project, "domain_id", None),
        "enabled": getattr(project, "is_enabled", getattr(project, "enabled", True)),
    }


def _user_view(user: object) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": getattr(user, "email", None),
        "default_project_id": getattr(user, "default_project_id", None),
        "domain_id": getattr(user, "domain_id", None),
        "enabled": getattr(user, "is_enabled", getattr(user, "enabled", True)),
    }


@router.get("/projects")
def list_projects(conn=Depends(get_openstack_conn)):
    """List Keystone projects."""
    try:
        return [_project_view(project) for project in conn.identity.projects()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/projects/{project_id}")
def get_project(project_id: str, conn=Depends(get_openstack_conn)):
    """Fetch a project."""
    try:
        project = conn.identity.get_project(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return _project_view(project)
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/users")
def list_users(conn=Depends(get_openstack_conn)):
    """List Keystone users."""
    try:
        return [_user_view(user) for user in conn.identity.users()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/users/{user_id}")
def get_user(user_id: str, conn=Depends(get_openstack_conn)):
    """Fetch a single user."""
    try:
        user = conn.identity.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return _user_view(user)
    except os_exc.ResourceNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from err
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

