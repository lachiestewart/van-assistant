from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from van_assistant.device_manager import DeviceManager

MAX_SEEN_DATA = 1000


class BaseScanner:
    """Base class for BLE scanners that detect and process manufacturer-specific advertisement data.

    This class provides a foundation for scanning BLE devices and handling their advertisement data.
    """

    def __init__(self, device_manager: DeviceManager) -> None:
        """Initialize the scanner.

        Args:
            device_manager: The DeviceManager instance to use for managing detected devices.

        """
        self.device_manager = device_manager

        self._scanner: BleakScanner = BleakScanner(
            detection_callback=self._detection_callback,
        )

        self._seen_data: set[bytes] = set()

    def _detection_callback(
        self,
        ble_device: BLEDevice,
        ad_data: AdvertisementData,
    ) -> None:
        """Handle a BLE advertisement detection event.

        Args:
            ble_device: The BLE device that was detected.
            ad_data: The advertisement data associated with the detected device.

        """
        for manufacturer_id, data in ad_data.manufacturer_data.items():
            if data in self._seen_data:
                continue

            # De-duplicate advertisements
            if len(self._seen_data) > MAX_SEEN_DATA:
                self._seen_data = set()
            self._seen_data.add(data)

            self.callback(manufacturer_id, ble_device, data)

    def callback(
        self,
        manufacturer_id: int,
        ble_device: BLEDevice,
        data: bytes,
    ) -> None:
        """Handle a detected BLE device.

        This method is called when a BLE device is detected and its advertisement data
        is processed. Subclasses should override this method to implement specific
        handling logic.

        Args:
            manufacturer_id: The manufacturer ID associated with the device.
            ble_device: The BLE device that was detected.
            data: The manufacturer-specific advertisement data.

        """

    async def start(self):
        await self._scanner.start()

    async def stop(self):
        await self._scanner.stop()
