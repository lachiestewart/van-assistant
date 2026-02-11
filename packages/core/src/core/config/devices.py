"""Device configuration models."""

from typing import Literal

from pydantic import BaseModel
from shared.brands import Brand


class BaseDeviceConfig(BaseModel):
    """Configuration for a single device."""

    name: str


class BLEDeviceConfig(BaseDeviceConfig):
    """Configuration for a BLE device."""

    mac_address: str
    encryption_key: str


class NetworkDeviceConfig(BaseDeviceConfig):
    """Configuration for a Wi-Fi or ethernet device."""

    ip_address: str


class VictronDeviceConfig(BLEDeviceConfig):
    """Configuration for a Victron device."""

    brand: Literal[Brand.VICTRON]


class RenogyDeviceConfig(NetworkDeviceConfig):
    """Configuration for a Renogy device."""

    brand: Literal[Brand.RENOGY]
