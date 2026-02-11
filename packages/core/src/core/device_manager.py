"""Device monitor for managing van device drivers."""

import logging

from core.config.config import VanConfig
from core.config.devices import BaseDeviceConfig
from core.drivers.base.device_driver import BaseDeviceDriver
from core.drivers.mqtt_client import MQTTClient

logger = logging.getLogger(__name__)


class DeviceManager:
    """Manages device drivers for all configured devices in the van.

    This class takes a VanConfig and instantiates the appropriate device drivers
    for each configured device (MPPT, DC-DC converter, charger, etc.).
    """

    def __init__(self, config: VanConfig, mqtt_client: MQTTClient) -> None:
        """Initialize the device manager with a van configuration.

        Args:
            config: Van configuration containing device definitions.
            mqtt_client: MQTT client for device communication.

        """
        self.config = config
        self.mqtt_client = mqtt_client
        self.drivers: list[BaseDeviceDriver] = []

        self._initialize_drivers()

    def _initialize_drivers(self) -> None:
        """Initialize device drivers based on configuration."""
        for device_config in self.config.devices:
            driver = self._create_driver(
                system_name=self.config.system.name,
                device_config=device_config,
            )
            self.drivers.append(driver)

    def _create_driver(
        self,
        system_name: str,
        device_config: BaseDeviceConfig,
    ) -> BaseDeviceDriver:
        """Create a device driver instance based on device configuration.

        Args:
            system_name: Name of the system.
            device_config: Configuration for the device.

        Returns:
            Instantiated device driver.

        Raises:
            ValueError: If the device name or connection type is not supported.

        """
        msg = "Device driver creation not yet implemented"
        raise NotImplementedError(msg)
