"""Service metadata endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get("/health")
def healthcheck():
    """Liveness probe endpoint."""
    return {"status": "ok"}

