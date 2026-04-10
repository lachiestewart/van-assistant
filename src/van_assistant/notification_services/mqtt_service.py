
import paho.mqtt.client as mqtt
from paho.mqtt.client import PayloadType

from van_assistant.notification_services.base import NotificationService


class MQTTService(NotificationService):
    def __init__(self, broker: str, port: int) -> None:
        self.client = mqtt.Client()
        self.client.connect(broker, port)

    def publish(self, topic: str, payload: PayloadType) -> None:
        self.client.publish(topic, payload)
        self.client.disconnect()
