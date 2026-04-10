from paho.mqtt.client import PayloadType

from van_assistant.notification_services.base import NotificationService


class LoggingService(NotificationService):
    def publish(self, topic: str, payload: PayloadType) -> None:
        print(f"Publishing to {topic}: {payload}")
