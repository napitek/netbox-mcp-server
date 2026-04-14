"""Tests for NetBoxRestClient write operations."""

from unittest.mock import MagicMock, patch

import pytest

from netbox_mcp_server.netbox_client import NetBoxRestClient


@pytest.fixture
def client():
    """Create a test client."""
    return NetBoxRestClient(
        url="https://netbox.example.com",
        token="test-token",
        verify_ssl=True,
    )


def test_bulk_create_uses_list_endpoint(client):
    """NetBox bulk create uses POST against the list endpoint."""
    response = MagicMock()
    response.json.return_value = [{"id": 1}]
    response.raise_for_status = MagicMock()

    with patch.object(client.session, "post", return_value=response) as mock_post:
        result = client.bulk_create("dcim/sites", [{"name": "Site A"}])

    assert result == [{"id": 1}]
    mock_post.assert_called_once_with(
        "https://netbox.example.com/api/dcim/sites/",
        json=[{"name": "Site A"}],
    )


def test_bulk_update_uses_list_endpoint(client):
    """NetBox bulk update uses PATCH against the list endpoint."""
    response = MagicMock()
    response.json.return_value = [{"id": 1, "status": "active"}]
    response.raise_for_status = MagicMock()

    with patch.object(client.session, "patch", return_value=response) as mock_patch:
        result = client.bulk_update("dcim/sites", [{"id": 1, "status": "active"}])

    assert result == [{"id": 1, "status": "active"}]
    mock_patch.assert_called_once_with(
        "https://netbox.example.com/api/dcim/sites/",
        json=[{"id": 1, "status": "active"}],
    )


def test_bulk_delete_uses_list_endpoint(client):
    """NetBox bulk delete uses DELETE against the list endpoint with IDs in the body."""
    response = MagicMock()
    response.status_code = 204
    response.raise_for_status = MagicMock()

    with patch.object(client.session, "request", return_value=response) as mock_request:
        result = client.bulk_delete("dcim/sites", [1, 2])

    assert result is True
    mock_request.assert_called_once_with(
        "DELETE",
        "https://netbox.example.com/api/dcim/sites/",
        json=[{"id": 1}, {"id": 2}],
    )
