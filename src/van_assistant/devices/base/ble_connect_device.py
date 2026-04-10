from abc import abstractmethod

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from van_assistant.devices.base.device import Device
from van_assistant.notification_services.base import NotificationService


class BLEConnectableDevice(Device):
    """Device that requires a BLE connection and may poll / receive notifications."""

    POLL_INTERVAL = 10.0

    def __init__(self, addr: str, notification_service: NotificationService) -> None:
        super().__init__(addr, notification_service)
        self._running = False
        self._client: BleakClient | None = None

    @abstractmethod
    async def _notify_handler(
        self,
        sender: BleakGATTCharacteristic,
        data: bytearray,
    ) -> None:
        """Handle incoming BLE notifications."""

    @abstractmethod
    def _get_notify_uuid(self) -> str:
        """Return the UUID to subscribe to for notifications."""

    @abstractmethod
    async def _run(self) -> None:
        """Main loop for polling or handling notifications."""

    async def start(self) -> None:
        """Establish BLE connection."""
        self._running = True

        self._client = BleakClient(self.addr)
        await self._client.connect()

        await self._client.start_notify(
            self._get_notify_uuid(),
            self._notify_handler,
        )

        await self._run()

    async def stop(self) -> None:
        """Disconnect BLE cleanly."""
        self._running = False
        if not self._client:
            return

        await self._client.stop_notify(self._get_notify_uuid())

        if self._client.is_connected:
            await self._client.disconnect()
