from abc import abstractmethod

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from van_assistant.devices.base.device import Device
from van_assistant.notification_services.base import NotificationService


class BLEConnectableDevice(Device):
    """Device that requires a BLE connection and may poll / receive notifications."""

    connectable = True

    def __init__(self, addr: str, notification_service: NotificationService) -> None:
        """Create a BLE connectable device.

        Args:
            addr: Unique identifier for the device, e.g. BLE MAC address.
            notification_service: Service to publish notifications to.

        """
        super().__init__(addr, notification_service)
        self._client = BleakClient(self.addr)
        self._running = False

    async def notify_handler(
        self,
        sender: BleakGATTCharacteristic,  # noqa: ARG002
        data: bytearray,
    ) -> None:
        """Handle incoming BLE notifications.

        Args:
            sender: The characteristic that sent the notification.
            data: The data received in the notification.

        """
        await self.handle_data(data)

    async def start(self) -> None:
        """Establish BLE connection."""
        self._running = True

        await self._client.connect()

        await self._client.start_notify(
            self.get_notify_uuid(),
            self.notify_handler,
        )

        await self.run()

    async def stop(self) -> None:
        """Disconnect BLE cleanly."""
        self._running = False

        await self._client.disconnect()

    @abstractmethod
    def get_notify_uuid(self) -> str:
        """Return the UUID to subscribe to for notifications."""

    @abstractmethod
    async def run(self) -> None:
        """Start polling device."""
