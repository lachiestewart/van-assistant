"""Base device driver class."""

from abc import ABC, abstractmethod

from core.drivers.mqtt_client import MQTTClient


class BaseDeviceDriver(ABC):
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

    @abstractmethod
    def start(self) -> None:
        """Start the device driver and perform any necessary initialization."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the device driver and perform any necessary cleanup."""

    @abstractmethod
    def read_data(self) -> dict:
        """Read data from the device.

        Returns:
            Dictionary containing device data.

        """
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)

    @abstractmethod
    def publish_status(self) -> None:
        """Publish device status to MQTT."""
        msg = "Must be implemented by subclass"
        raise NotImplementedError(msg)
