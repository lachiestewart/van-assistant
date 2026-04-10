import logging

from paho.mqtt.client import PayloadType

from van_assistant.notification_services.base import NotificationService

logger = logging.getLogger(__name__)


class LoggingService(NotificationService):
    """Notification service that logs notifications to the console."""

    def publish(self, topic: str, payload: PayloadType) -> None:
        """Log the notification to the console.

        Args:
            topic: The topic of the notification.
            payload: The payload of the notification.

        """
        logger.info(f"Publishing to {topic}: {payload}")
