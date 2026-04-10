import asyncio
from abc import abstractmethod
from itertools import cycle

from van_assistant.devices.base.ble_connect_device import BLEConnectableDevice
from van_assistant.notification_services.base import NotificationService

NOTIFY_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

PACKET_HEADER = 0xDD
PACKET_TAIL = 0x77

POLL_INTERVAL = 5.0


class RemcoDevice(BLEConnectableDevice):
    """BLE connectable device for Remco BMS units."""

    def __init__(self, addr: str, notification_service: NotificationService) -> None:
        """Create a Remco BMS device.

        Args:
            addr: Unique identifier for the device, e.g. BLE MAC address.
            notification_service: Service to publish notifications to.

        """
        super().__init__(addr, notification_service)
        self._packet_buffer: bytearray = bytearray()

    def get_notify_uuid(self) -> str:
        """Return the UUID to subscribe to for notifications."""
        return NOTIFY_UUID

    async def run(self) -> None:
        """Start polling device."""
        for cmd in cycle(self.get_commands()):
            if not self._running:
                break

            await self._client.write_gatt_char(
                WRITE_UUID,
                cmd,
                response=False,
            )
            await asyncio.sleep(POLL_INTERVAL)

    async def handle_data(
        self,
        data: bytes | bytearray,
    ) -> None:
        """Handle incoming BLE notifications.

        Args:
            data: The raw data received from the BLE notification.

        """
        self._packet_buffer.extend(data)

        if len(self._packet_buffer) == 0:
            return

        if self._packet_buffer[0] != PACKET_HEADER:
            self._packet_buffer.clear()
            return

        if self._packet_buffer[-1] == PACKET_TAIL:
            self.parse(self._packet_buffer.copy())
            self._packet_buffer.clear()

    @abstractmethod
    def parse(self, packet: bytearray) -> None:
        """Parse a complete packet from the device.

        Args:
            packet: The complete packet data to parse.

        """

    @abstractmethod
    def get_commands(self) -> list[bytes]:
        """Return the list of commands to poll from the device."""
