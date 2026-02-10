"""MQTT client protocol."""


class MQTTClient:
    """Protocol for MQTT client dependency."""

    def publish(self, topic: str, payload: str) -> None:
        """Publish a message to an MQTT topic."""

    def subscribe(self, topic: str) -> None:
        """Subscribe to an MQTT topic."""
