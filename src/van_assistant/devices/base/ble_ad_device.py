from van_assistant.devices.base.device import Device


class BLEAdvertisementDevice(Device):
    """Device that only listens to BLE advertisements, no connection needed."""

    connectable = False
