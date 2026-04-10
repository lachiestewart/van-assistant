import logging

from bleak.backends.device import BLEDevice

from van_assistant.devices.brands import SupportedBrand
from van_assistant.scanners.base_scanner import BaseScanner
from van_assistant.util.bluetooth_providers import COMPANY_IDS

logger = logging.getLogger(__name__)


class DeviceScanner(BaseScanner):
    """Scanner for BLE devices that identifies supported brands."""

    def get_brand_name(self, manufacturer_id: int) -> str | None:
        """Get the brand name associated with a manufacturer ID.

        Args:
            manufacturer_id: The manufacturer ID to look up.

        Returns:
            The brand name associated with the manufacturer ID, or None if not found.

        """
        brand_name = COMPANY_IDS.get(manufacturer_id)
        if brand_name is None:
            logger.info(f"Unknown manufacturer ID: {manufacturer_id}")
            return None
        return brand_name

    def get_supported_brand(self, brand_name: str) -> SupportedBrand | None:
        """Get the SupportedBrand enum member associated with a brand name.

        Args:
            brand_name: The brand name to look up.

        Returns:
            The SupportedBrand enum member associated with the brand name if supported.

        """
        try:
            return SupportedBrand(brand_name)
        except ValueError:
            logger.info(f"Brand not supported: {brand_name}")

    def callback(
        self,
        manufacturer_id: int,
        ble_device: BLEDevice,
        data: bytes,  # noqa: ARG002
    ) -> None:
        """Handle a detected BLE device.

        Args:
            manufacturer_id: The manufacturer ID associated with the device.
            ble_device: The BLE device that was detected.
            data: The advertisement data associated with the detected device.

        """
        logger.info(f"Detected {ble_device}")

        brand_name = self.get_brand_name(manufacturer_id)
        if brand_name is None:
            return

        supported_brand = self.get_supported_brand(brand_name)
        if supported_brand is None:
            return

        logger.info(f"Detected supported brand: {supported_brand.value} ({brand_name})")
