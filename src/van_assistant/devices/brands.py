from enum import StrEnum

from van_assistant.devices.base.identifier import DeviceIdentifier
from van_assistant.devices.remco.identifier import RemcoDeviceIdentifier
from van_assistant.devices.victron.identifier import VictronDeviceIdentifier


class SupportedBrand(StrEnum):
    """Enum of supported device brands."""

    VICTRON = "Victron Energy BV"
    REMCO = "Remco Energy"


SUPPORTED_BRANDS: set[SupportedBrand] = {
    SupportedBrand.VICTRON,
    SupportedBrand.REMCO,
}

BRAND_TO_IDENTIFIER: dict[SupportedBrand, type[DeviceIdentifier]] = {
    SupportedBrand.VICTRON: VictronDeviceIdentifier,
    SupportedBrand.REMCO: RemcoDeviceIdentifier,
}
