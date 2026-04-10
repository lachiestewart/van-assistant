from bleak.backends.device import BLEDevice

from van_assistant.devices.brands import SupportedBrand
from van_assistant.scanners.base_scanner import BaseScanner
from van_assistant.util.bluetooth_providers import COMPANY_IDS


class DeviceScanner(BaseScanner):
    def _get_brand_name(self, manufacturer_id: int) -> str | None:
        brand_name = COMPANY_IDS.get(manufacturer_id)
        if brand_name is None:
            print(f"Unknown manufacturer ID: {manufacturer_id}")
            return None
        return brand_name

    def _get_supported_brand(self, brand_name: str) -> SupportedBrand | None:
        try:
            return SupportedBrand(brand_name)
        except ValueError:
            print(f"Brand not supported: {brand_name}")

    def callback(
        self,
        manufacturer_id: int,
        ble_device: BLEDevice,
        data: bytes,
    ) -> None:

        print(f"Detected {ble_device}")

        brand_name = self._get_brand_name(manufacturer_id)
        if brand_name is None:
            return

        supported_brand = self._get_supported_brand(brand_name)
        if supported_brand is None:
            return

        device = self.device_manager.get_device(ble_device.address)

        if not device:
            print(f"Adding new device: {ble_device.address} ({brand_name})")
            device = self.device_manager.add_device(ble_device.address, supported_brand)

        if not device:
            print(f"Failed to add device: {ble_device.address} ({brand_name})")
            return

        print(
            f"Notifying device: {ble_device.address} ({brand_name}) with data: {data.hex(' ')}",
        )
        device.handle_advertisement(data)
