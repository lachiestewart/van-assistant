"""Factory for creating device drivers based on configuration."""

from packages.core.src.core.config.config import (
    BaseDeviceConfig,
    RenogyDeviceConfig,
    VictronDeviceConfig,
)
from packages.shared.src.shared.mqtt import MQTTClient

from .base.device_driver import BaseDeviceDriver
from .renogy.renogy_network_driver import RenogyNetworkDriver
from .victron.victron_ble_driver import VictronBLEDriver


class DriverFactory:
    """Factory class for creating device drivers.

    This factory creates the appropriate driver instance based on the
    device configuration type.
    """

    @staticmethod
    def create_driver(
        system_name: str,
        device_config: BaseDeviceConfig,
        mqtt_client: MQTTClient,
    ) -> BaseDeviceDriver:
        """Create a device driver based on configuration.

        Args:
            system_name: Name of the system (e.g., "Dora").
            device_config: Configuration for the device.
            mqtt_client: MQTT client for communication.

        Returns:
            Instantiated device driver.

        Raises:
            ValueError: If the device configuration type is not supported.

        """
        if isinstance(device_config, VictronDeviceConfig):
            return VictronBLEDriver(
                system_name=system_name,
                mac_address=device_config.mac_address,
                encryption_key=device_config.encryption_key,
                device_name=device_config.name,
                mqtt_client=mqtt_client,
            )
        if isinstance(device_config, RenogyDeviceConfig):
            return RenogyNetworkDriver(
                system_name=system_name,
                ip_address=device_config.ip_address,
                device_name=device_config.name,
                mqtt_client=mqtt_client,
            )
        msg = f"Unsupported device: {device_config}"
        raise ValueError(msg)
