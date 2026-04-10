from abc import ABC, abstractmethod

from van_assistant.devices.base.device import Device


class DeviceIdentifier(ABC):
    """Base class for device identifiers."""

    @staticmethod
    @abstractmethod
    def get_device_type(data: bytes | bytearray) -> type[Device]:
        """Return the device type based on the raw data."""
