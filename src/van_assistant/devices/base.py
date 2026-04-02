import abc
from enum import StrEnum

from van_assistant.bluetooth_providers import COMPANY_IDS


class SupportedBrand(StrEnum):
    VICTRON = "Victron Energy BV"


SUPPORTED_BRANDS: set[SupportedBrand] = {
    SupportedBrand.VICTRON,
}


def get_supported_brand(manufacturer_id: int) -> SupportedBrand | None:
    if manufacturer_id not in COMPANY_IDS:
        return None
    brand_name = COMPANY_IDS[manufacturer_id]

    brand = None
    try:
        brand = SupportedBrand(brand_name)
    except ValueError:
        print(f"Brand not supported: {brand_name}")

    return brand


class Device(abc.ABC):
    pass
