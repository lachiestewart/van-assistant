from dataclasses import dataclass

from van_assistant.devices.base.device_data import DeviceData


@dataclass
class Event:
    topic: str
    payload: DeviceData
