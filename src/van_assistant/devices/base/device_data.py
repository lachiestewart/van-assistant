from dataclasses import dataclass
from typing import Any


@dataclass
class DeviceData:
    data: dict[str, Any]
