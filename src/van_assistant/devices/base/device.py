from abc import ABC, abstractmethod

from van_assistant.notification_services.base import NotificationService


class Device(ABC):
    def __init__(self, addr: str, notification_service: NotificationService) -> None:
        self.addr = addr
        self.notification_service = notification_service
        self.is_active = False

    @abstractmethod
    async def start(self):
        """Start the device task (polling or handling readouts)."""

    @abstractmethod
    async def stop(self):
        """Stop the device task and disconnect if needed."""
