from van_assistant.devices.base.device import Device
from van_assistant.devices.brands import SupportedBrand
from van_assistant.devices.remco.base import RemcoDevice

BRAND_DEVICE_MAP: dict[SupportedBrand, type[Device]] = {
    SupportedBrand.REMCO: RemcoDevice,
}


class DeviceManager:
    def __init__(self, notification_service: NotificationService):
        self.devices: list[Device] = []
        self.mqtt_service = mqtt_service

    def add_device(self, addr: str, brand: SupportedBrand) -> Device | None:
        device_type = BRAND_DEVICE_MAP.get(brand)
        if not device_type:
            print(f"No Device handler for brand: {brand}")
            return None

        device = device_type(addr, self.mqtt_service)
        self.devices.append(device)

        return device

    def get_device(self, addr: str) -> Device | None:
        for device in self.devices:
            if device.addr == addr:
                return device
        return None
