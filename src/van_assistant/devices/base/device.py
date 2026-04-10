from abc import ABC, abstractmethod

from van_assistant.notification_services.base import NotificationService


class Device(ABC):
    """Base class for all Bluetooth devices."""

    connectable = False

    def __init__(
        self,
        addr: str,
        notification_service: NotificationService,
        encryption_key: str | None = None,
    ) -> None:
        """Represent a base class for all devices.

        Args:
            addr: Unique identifier for the device, e.g. BLE MAC address.
            notification_service: Service to publish notifications to.
            encryption_key: Key for encrypting/decrypting data, if applicable.

        """
        self.addr = addr
        self.notification_service = notification_service
        self.encryption_key = encryption_key

    @abstractmethod
    async def start(self) -> None:
        """Start the device, e.g. connect or start scanning."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the device, e.g. disconnect or stop scanning."""

    @abstractmethod
    async def handle_data(self, data: bytes | bytearray) -> None:
        """Handle incoming data from the device."""
