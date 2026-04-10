import paho.mqtt.client as mqtt
from paho.mqtt.client import PayloadType

from van_assistant.notification_services.base import NotificationService


class MQTTService(NotificationService):
    """Notification service that publishes notifications to an MQTT broker."""

    def __init__(self, broker: str, port: int) -> None:
        """Initialize the MQTT client and connect to the broker.

        Args:
            broker: The address of the MQTT broker.
            port: The port to connect to on the MQTT broker.

        """
        self.client = mqtt.Client()
        self.client.connect(broker, port)

    def publish(self, topic: str, payload: PayloadType) -> None:
        """Publish the notification to the MQTT broker.

        Args:
            topic: The topic of the notification.
            payload: The payload of the notification.

        """
        self.client.publish(topic, payload)
        self.client.disconnect()
