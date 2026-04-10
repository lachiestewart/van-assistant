from van_assistant.devices.base.identifier import DeviceIdentifier
from van_assistant.devices.remco.devices.base import RemcoDevice
from van_assistant.devices.remco.devices.bms import RemcoBattery


class RemcoDeviceIdentifier(DeviceIdentifier):
    """Identifier for Remco devices."""

    @staticmethod
    def get_device_type(data: bytes | bytearray) -> type[RemcoDevice]:  # noqa: ARG004
        """Return the device type based on the raw data."""
        return RemcoBattery
