"""Tests for write-capable MCP tools."""

from unittest.mock import patch

import pytest

from netbox_mcp_server.server import (
    netbox_bulk_create_objects,
    netbox_bulk_delete_objects,
    netbox_bulk_update_objects,
    netbox_create_object,
    netbox_delete_object,
    netbox_get_write_requirements,
    netbox_update_object,
)


def test_create_requires_writes_enabled():
    """Create operations should be blocked when writes are disabled."""
    with pytest.raises(PermissionError, match="write operations are disabled"):
        netbox_create_object("dcim.site", {"name": "Site A", "slug": "site-a"})


def test_get_write_requirements_returns_curated_schema():
    """Write requirements should guide create payload collection."""
    result = netbox_get_write_requirements("ipam.ipaddress")

    assert result["object_type"] == "ipam.ipaddress"
    assert result["schema_available"] is True
    assert result["required_fields"] == ["address"]
    assert result["example"]["address"] == "192.0.2.10/24"


def test_get_write_requirements_returns_missing_schema_response():
    """Object types without a curated schema should return a clear response."""
    result = netbox_get_write_requirements("core.objectchange")

    assert result["object_type"] == "core.objectchange"
    assert result["schema_available"] is False
    assert result["required_fields"] == []


@patch("netbox_mcp_server.server.netbox")
def test_create_rejects_missing_curated_required_fields(mock_netbox):
    """Create should fail before the API call when a curated required field is missing."""
    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="address"),
    ):
        netbox_create_object("ipam.ipaddress", {"status": "active"})

    mock_netbox.create.assert_not_called()


@patch("netbox_mcp_server.server.netbox")
def test_create_object_calls_client(mock_netbox):
    """Create should route to the mapped NetBox endpoint."""
    mock_netbox.create.return_value = {"id": 1, "name": "Site A"}

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_create_object("dcim.site", {"name": "Site A", "slug": "site-a"})

    assert result == {"id": 1, "name": "Site A"}
    mock_netbox.create.assert_called_once_with(
        "dcim/sites",
        data={"name": "Site A", "slug": "site-a"},
    )


@patch("netbox_mcp_server.server.netbox")
def test_update_object_calls_client(mock_netbox):
    """Update should use PATCH through the client."""
    mock_netbox.update.return_value = {"id": 42, "status": "active"}

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_update_object("dcim.device", 42, {"status": "active"})

    assert result == {"id": 42, "status": "active"}
    mock_netbox.update.assert_called_once_with(
        "dcim/devices",
        id=42,
        data={"status": "active"},
    )


def test_update_rejects_mismatched_id():
    """Object ID mismatches are ambiguous and should be rejected."""
    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="must match object_id"),
    ):
        netbox_update_object("dcim.device", 42, {"id": 43, "status": "active"})


def test_delete_requires_confirmation():
    """Delete should require an explicit confirmation parameter."""
    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="confirm=True"),
    ):
        netbox_delete_object("dcim.device", 42)


@patch("netbox_mcp_server.server.netbox")
def test_delete_object_calls_client(mock_netbox):
    """Delete should route to the mapped NetBox endpoint."""
    mock_netbox.delete.return_value = True

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_delete_object("dcim.device", 42, confirm=True)

    assert result == {"deleted": True, "object_type": "dcim.device", "object_id": 42}
    mock_netbox.delete.assert_called_once_with("dcim/devices", id=42)


@patch("netbox_mcp_server.server.netbox")
def test_bulk_create_objects_calls_client(mock_netbox):
    """Bulk create should route the list payload to the client."""
    payload = [{"name": "Site A", "slug": "site-a"}]
    mock_netbox.bulk_create.return_value = [{"id": 1, "name": "Site A"}]

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_bulk_create_objects("dcim.site", payload)

    assert result == [{"id": 1, "name": "Site A"}]
    mock_netbox.bulk_create.assert_called_once_with("dcim/sites", data=payload)


@patch("netbox_mcp_server.server.netbox")
def test_bulk_create_rejects_missing_curated_required_fields(mock_netbox):
    """Bulk create should identify the failing item when curated required fields are missing."""
    payload = [{"address": "192.0.2.10/24"}, {"status": "active"}]

    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="bulk item 1"),
    ):
        netbox_bulk_create_objects("ipam.ipaddress", payload)

    mock_netbox.bulk_create.assert_not_called()


@patch("netbox_mcp_server.server.netbox")
def test_bulk_update_objects_calls_client(mock_netbox):
    """Bulk update should require IDs and route to the client."""
    payload = [{"id": 1, "status": "active"}, {"id": 2, "status": "planned"}]
    mock_netbox.bulk_update.return_value = payload

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_bulk_update_objects("dcim.site", payload)

    assert result == payload
    mock_netbox.bulk_update.assert_called_once_with("dcim/sites", data=payload)


def test_bulk_update_requires_ids():
    """Bulk updates require each object to include an ID."""
    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="positive integer 'id'"),
    ):
        netbox_bulk_update_objects("dcim.site", [{"status": "active"}])


@patch("netbox_mcp_server.server.netbox")
def test_bulk_delete_objects_calls_client(mock_netbox):
    """Bulk delete should require confirmation and route IDs to the client."""
    mock_netbox.bulk_delete.return_value = True

    with patch("netbox_mcp_server.server.enable_writes", True):
        result = netbox_bulk_delete_objects("dcim.site", [1, 2], confirm=True)

    assert result == {
        "deleted": True,
        "object_type": "dcim.site",
        "object_ids": [1, 2],
        "count": 2,
    }
    mock_netbox.bulk_delete.assert_called_once_with("dcim/sites", ids=[1, 2])


def test_bulk_delete_requires_confirmation():
    """Bulk delete should require an explicit confirmation parameter."""
    with (
        patch("netbox_mcp_server.server.enable_writes", True),
        pytest.raises(ValueError, match="confirm=True"),
    ):
        netbox_bulk_delete_objects("dcim.site", [1, 2])
