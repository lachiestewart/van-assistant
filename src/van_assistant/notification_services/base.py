from abc import ABC, abstractmethod

from paho.mqtt.client import PayloadType


class NotificationService(ABC):
    @abstractmethod
    def publish(self, topic: str, payload: PayloadType) -> None:
        """Publish a notification to the service."""
