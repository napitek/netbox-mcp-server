"""Curated write requirements for common NetBox object types."""

from typing import Any, TypedDict


class NetBoxWriteSchema(TypedDict):
    """Metadata used to guide and validate common NetBox create operations."""

    required_fields: tuple[str, ...]
    recommended_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    example: dict[str, Any]
    notes: tuple[str, ...]


NETBOX_WRITE_SCHEMAS: dict[str, NetBoxWriteSchema] = {
    "circuits.circuit": {
        "required_fields": ("cid", "provider", "type"),
        "recommended_fields": ("status", "description"),
        "optional_fields": ("tenant", "install_date", "termination_a", "termination_z", "tags"),
        "example": {
            "cid": "CIR-1001",
            "provider": 1,
            "type": 1,
            "status": "active",
        },
        "notes": (
            "Use numeric IDs or unique object dictionaries for provider and type.",
            "Add changelog_message when you want an audit note.",
        ),
    },
    "circuits.circuittype": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("description", "tags"),
        "example": {"name": "Transit", "slug": "transit"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "circuits.provider": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("description", "comments", "tags"),
        "example": {"name": "Example Provider", "slug": "example-provider"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "dcim.device": {
        "required_fields": ("name", "device_type", "role", "site"),
        "recommended_fields": ("status", "platform"),
        "optional_fields": ("rack", "position", "face", "serial", "asset_tag", "tenant", "tags"),
        "example": {
            "name": "switch01",
            "device_type": 1,
            "role": 1,
            "site": 1,
            "status": "active",
        },
        "notes": (
            "Use numeric IDs or unique object dictionaries for device_type, role, site, and rack.",
            "Use dcim.devicetype, dcim.devicerole, and dcim.site lookups before creating devices.",
        ),
    },
    "dcim.devicerole": {
        "required_fields": ("name", "slug"),
        "recommended_fields": ("color",),
        "optional_fields": ("description", "tags"),
        "example": {"name": "Switch", "slug": "switch", "color": "2196f3"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "dcim.devicetype": {
        "required_fields": ("manufacturer", "model", "slug"),
        "recommended_fields": (),
        "optional_fields": ("part_number", "u_height", "is_full_depth", "comments", "tags"),
        "example": {"manufacturer": 1, "model": "DCS-7280", "slug": "dcs-7280"},
        "notes": ("Use a numeric ID or unique object dictionary for manufacturer.",),
    },
    "dcim.interface": {
        "required_fields": ("device", "name", "type"),
        "recommended_fields": ("enabled",),
        "optional_fields": ("description", "mac_address", "mtu", "mode", "untagged_vlan", "tags"),
        "example": {"device": 1, "name": "Ethernet1", "type": "1000base-t", "enabled": True},
        "notes": ("Use a numeric ID or unique object dictionary for device.",),
    },
    "dcim.location": {
        "required_fields": ("name", "slug", "site"),
        "recommended_fields": (),
        "optional_fields": ("parent", "status", "description", "tags"),
        "example": {"name": "Room 101", "slug": "room-101", "site": 1},
        "notes": ("Use a numeric ID or unique object dictionary for site and parent.",),
    },
    "dcim.manufacturer": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("description", "tags"),
        "example": {"name": "Example Networks", "slug": "example-networks"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "dcim.platform": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("manufacturer", "description", "tags"),
        "example": {"name": "EOS", "slug": "eos"},
        "notes": ("Use a numeric ID or unique object dictionary for manufacturer when provided.",),
    },
    "dcim.rack": {
        "required_fields": ("name", "site"),
        "recommended_fields": ("status",),
        "optional_fields": ("location", "role", "facility_id", "u_height", "tenant", "tags"),
        "example": {"name": "R101", "site": 1, "status": "active"},
        "notes": ("Use numeric IDs or unique object dictionaries for site, location, and role.",),
    },
    "dcim.region": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("parent", "description", "tags"),
        "example": {"name": "Europe", "slug": "europe"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "dcim.site": {
        "required_fields": ("name", "slug"),
        "recommended_fields": ("status",),
        "optional_fields": ("region", "group", "tenant", "facility", "description", "tags"),
        "example": {"name": "Milan Lab", "slug": "milan-lab", "status": "active"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "dcim.sitegroup": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("parent", "description", "tags"),
        "example": {"name": "Labs", "slug": "labs"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "extras.tag": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("color", "description"),
        "example": {"name": "MCP Created", "slug": "mcp-created"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "ipam.ipaddress": {
        "required_fields": ("address",),
        "recommended_fields": ("status", "description"),
        "optional_fields": (
            "vrf",
            "tenant",
            "dns_name",
            "assigned_object_type",
            "assigned_object_id",
            "tags",
        ),
        "example": {
            "address": "192.0.2.10/24",
            "status": "active",
            "description": "Created by MCP",
        },
        "notes": (
            "Use assigned_object_type and assigned_object_id only when assigning to an interface.",
            "Use a numeric ID or unique object dictionary for vrf and tenant when provided.",
        ),
    },
    "ipam.prefix": {
        "required_fields": ("prefix",),
        "recommended_fields": ("status", "description"),
        "optional_fields": ("vrf", "scope_type", "scope_id", "tenant", "vlan", "role", "tags"),
        "example": {"prefix": "192.0.2.0/24", "status": "active"},
        "notes": ("Use vrf, scope_type, and scope_id only when the prefix belongs to a scope.",),
    },
    "ipam.vlan": {
        "required_fields": ("vid", "name"),
        "recommended_fields": ("status",),
        "optional_fields": ("group", "site", "tenant", "role", "description", "tags"),
        "example": {"vid": 100, "name": "Users", "status": "active"},
        "notes": (
            "VID must be an integer. Use a numeric ID or unique object dictionary for group.",
        ),
    },
    "ipam.vrf": {
        "required_fields": ("name",),
        "recommended_fields": (),
        "optional_fields": ("rd", "tenant", "description", "tags"),
        "example": {"name": "Customer-A", "rd": "65000:100"},
        "notes": ("Route distinguisher is optional in NetBox but often useful operationally.",),
    },
    "tenancy.tenant": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("group", "description", "comments", "tags"),
        "example": {"name": "Customer A", "slug": "customer-a"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "virtualization.cluster": {
        "required_fields": ("name", "type"),
        "recommended_fields": ("status",),
        "optional_fields": ("group", "site", "tenant", "description", "tags"),
        "example": {"name": "Cluster A", "type": 1, "status": "active"},
        "notes": ("Use a numeric ID or unique object dictionary for type.",),
    },
    "virtualization.clustergroup": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("description", "tags"),
        "example": {"name": "VMware", "slug": "vmware"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "virtualization.clustertype": {
        "required_fields": ("name", "slug"),
        "recommended_fields": (),
        "optional_fields": ("description", "tags"),
        "example": {"name": "VMware vSphere", "slug": "vmware-vsphere"},
        "notes": ("Slugs should be URL-safe and unique for this object type.",),
    },
    "virtualization.virtualmachine": {
        "required_fields": ("name",),
        "recommended_fields": ("status", "cluster"),
        "optional_fields": ("role", "tenant", "platform", "vcpus", "memory", "disk", "tags"),
        "example": {"name": "vm01", "status": "active", "cluster": 1},
        "notes": ("Use a numeric ID or unique object dictionary for cluster when provided.",),
    },
    "virtualization.vminterface": {
        "required_fields": ("virtual_machine", "name"),
        "recommended_fields": ("enabled",),
        "optional_fields": ("description", "mac_address", "mtu", "mode", "untagged_vlan", "tags"),
        "example": {"virtual_machine": 1, "name": "eth0", "enabled": True},
        "notes": ("Use a numeric ID or unique object dictionary for virtual_machine.",),
    },
    "vpn.tunnel": {
        "required_fields": ("name", "status"),
        "recommended_fields": (),
        "optional_fields": (
            "group",
            "encapsulation",
            "ipsec_profile",
            "tenant",
            "description",
            "tags",
        ),
        "example": {"name": "Tunnel 1", "status": "active"},
        "notes": ("Use numeric IDs or unique object dictionaries for group and ipsec_profile.",),
    },
    "wireless.wirelesslan": {
        "required_fields": ("ssid",),
        "recommended_fields": ("status",),
        "optional_fields": ("group", "vlan", "auth_type", "description", "tags"),
        "example": {"ssid": "Corp-WiFi", "status": "active"},
        "notes": (
            "Use a numeric ID or unique object dictionary for group and vlan when provided.",
        ),
    },
}


def get_write_requirements(object_type: str) -> dict[str, Any]:
    """Return write guidance for an object type."""
    schema = NETBOX_WRITE_SCHEMAS.get(object_type)
    if schema is None:
        return {
            "object_type": object_type,
            "schema_available": False,
            "required_fields": [],
            "recommended_fields": [],
            "optional_fields": [],
            "example": {},
            "notes": [
                "No curated write schema is available for this object type.",
                "Use NetBox API validation errors or add a schema entry for this type.",
            ],
        }

    return {
        "object_type": object_type,
        "schema_available": True,
        "required_fields": list(schema["required_fields"]),
        "recommended_fields": list(schema["recommended_fields"]),
        "optional_fields": list(schema["optional_fields"]),
        "example": schema["example"].copy(),
        "notes": list(schema["notes"]),
    }


def validate_create_payload(
    object_type: str,
    data: dict[str, Any],
    index: int | None = None,
) -> None:
    """Validate MCP-curated required fields for create payloads when a schema exists."""
    schema = NETBOX_WRITE_SCHEMAS.get(object_type)
    if schema is None:
        return

    missing_fields = [
        field_name
        for field_name in schema["required_fields"]
        if not _has_required_value(data, field_name)
    ]
    if not missing_fields:
        return

    item_context = f" at bulk item {index}" if index is not None else ""
    raise ValueError(
        f"Missing required field(s) for {object_type}{item_context}: "
        f"{', '.join(missing_fields)}. Call netbox_get_write_requirements('{object_type}') "
        "to see the expected create payload."
    )


def _has_required_value(data: dict[str, Any], field_name: str) -> bool:
    """Return whether a required field is present and not empty."""
    if field_name not in data:
        return False

    value = data[field_name]
    if value is None:
        return False
    if isinstance(value, str) and value == "":
        return False
    return True
