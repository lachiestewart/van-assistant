"""Base device driver class."""

from packages.shared.src.shared.mqtt import MQTTClient


class BaseDeviceDriver:
    """Base class for device drivers.

    This abstract base class defines the interface that all device driver
    implementations must follow.
    """

    def __init__(self, name: str, mqtt_client: MQTTClient) -> None:
        """Initialize the base device driver.

        Args:
            name: Name of the device driver instance.
            mqtt_client: MQTT client for communication.

        """
        self.name = name
        self.mqtt_client = mqtt_client

    def read_data(self) -> dict:
        """Read data from the device.

        Returns:
            Dictionary containing device data.

        """
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)

    def publish_status(self) -> None:
        """Publish device status to MQTT."""
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)
