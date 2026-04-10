from abc import abstractmethod

from van_assistant.devices.base.device import Device
from van_assistant.notification_services.base import NotificationService


class BLEAdvertisementDevice(Device):
    """Device that only listens to BLE advertisements, no connection needed."""

    def __init__(self, addr: str, notification_service: NotificationService):
        super().__init__(addr, notification_service)

    @abstractmethod
    def parse_advertisement(self, data: bytes) -> None:
        pass

    async def handle_advertisement(self, data: bytes) -> None:
        print(f"[{self.addr}] Advertisement: {data.hex()}")
