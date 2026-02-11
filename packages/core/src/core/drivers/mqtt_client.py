"""MQTT client wrapper for aiomqtt."""

import asyncio

from aiomqtt import Client as AIOMQTTClient

from core.config.settings import Settings


class MQTTClient:
    """MQTT client for publishing and subscribing to topics.

    This class wraps the aiomqtt Client to provide a simplified interface
    for MQTT communication in the van assistant system.
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Initialize the MQTT client.

        Args:
            host: MQTT broker hostname or IP address.
            port: MQTT broker port.
            username: Optional username for authentication.
            password: Optional password for authentication.

        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = AIOMQTTClient(
            hostname=host,
            port=port,
            username=username,
            password=password,
        )

    async def connect(self) -> None:
        """Connect to the MQTT broker."""
        await self.client.__aenter__()

    async def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        await self.client.__aexit__(None, None, None)

    async def publish(self, topic: str, payload: str) -> None:
        """Publish a message to a topic.

        Args:
            topic: MQTT topic to publish to.
            payload: Message payload as string.

        """
        await self.client.publish(topic, payload)

    async def subscribe(self, topic: str) -> None:
        """Subscribe to a topic.

        Args:
            topic: MQTT topic to subscribe to.

        """
        await self.client.subscribe(topic)

    async def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic.

        Args:
            topic: MQTT topic to unsubscribe from.

        """
        await self.client.unsubscribe(topic)


async def main() -> None:
    settings = Settings()

    async with AIOMQTTClient(
        hostname=settings.mqtt_host,
        port=settings.mqtt_port,
        username=settings.mqtt_username,
        password=settings.mqtt_password,
    ) as mqtt_client:
        await mqtt_client.publish("test/topic", "Hello, MQTT!")
        await mqtt_client.subscribe("test/topic")


if __name__ == "__main__":
    asyncio.run(main())
