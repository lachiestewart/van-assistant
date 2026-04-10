from dataclasses import dataclass
from typing import Any


@dataclass
class DeviceData:
    """Data class for device data."""

    data: dict[str, Any]
