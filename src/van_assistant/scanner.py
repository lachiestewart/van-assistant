from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from van_assistant.devices.base import SupportedBrand, get_supported_brand

MAX_SEEN_DATA = 1000


class DeviceScanner:
    def __init__(self) -> None:
        """Initialize the scanner."""
        self._scanner: BleakScanner = BleakScanner(
            detection_callback=self._detection_callback,
        )
        self._seen_data: set[bytes] = set()

    def _detection_callback(
        self,
        device: BLEDevice,
        advertisement: AdvertisementData,
    ) -> None:
        """Handle a BLE advertisement detection event.

        Args:
            device: The BLE device that was detected.
            advertisement: The advertisement data associated with the detected device.

        """
        for manufacturer_id, data in advertisement.manufacturer_data.items():
            if data in self._seen_data:
                continue

            brand = get_supported_brand(manufacturer_id)
            if brand is None:
                continue

            # De-duplicate advertisements
            if len(self._seen_data) > MAX_SEEN_DATA:
                self._seen_data = set()
            self._seen_data.add(data)

            self.callback(brand, device, data)

    def callback(
        self,
        brand: SupportedBrand,
        device: BLEDevice,
        data: bytes,
    ) -> None:
        pass

    async def start(self):
        await self._scanner.start()

    async def stop(self):
        await self._scanner.stop()
