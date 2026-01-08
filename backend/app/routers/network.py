"""Network (Neutron) operations."""

from fastapi import APIRouter, Depends, HTTPException
from openstack import exceptions as os_exc
from app.dependencies.openstack import get_openstack_conn

router = APIRouter(prefix="/network", tags=["network"])


def _network_view(network: object) -> dict:
    return {
        "id": network.id,
        "name": network.name,
        "status": network.status,
        "project_id": getattr(network, "project_id", None),
        "shared": getattr(network, "is_shared", getattr(network, "shared", False)),
        "external": getattr(network, "is_router_external", getattr(network, "router:external", False)),
    }


def _subnet_view(subnet: object) -> dict:
    return {
        "id": subnet.id,
        "name": subnet.name,
        "cidr": getattr(subnet, "cidr", None),
        "gateway_ip": getattr(subnet, "gateway_ip", None),
        "ip_version": getattr(subnet, "ip_version", None),
        "network_id": getattr(subnet, "network_id", None),
    }


def _security_group_view(secgroup: object) -> dict:
    return {
        "id": secgroup.id,
        "name": secgroup.name,
        "description": getattr(secgroup, "description", ""),
        "project_id": getattr(secgroup, "project_id", None),
    }


@router.get("/networks")
def list_networks(conn=Depends(get_openstack_conn)):
    """List Neutron networks."""
    try:
        return [_network_view(net) for net in conn.network.networks()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/subnets")
def list_subnets(conn=Depends(get_openstack_conn)):
    """List Neutron subnets."""
    try:
        return [_subnet_view(sub) for sub in conn.network.subnets()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err


@router.get("/security-groups")
def list_security_groups(conn=Depends(get_openstack_conn)):
    """List Neutron security groups."""
    try:
        return [_security_group_view(sg) for sg in conn.network.security_groups()]
    except os_exc.SDKException as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

