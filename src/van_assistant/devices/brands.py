from enum import StrEnum


class SupportedBrand(StrEnum):
    VICTRON = "Victron Energy BV"
    REMCO = "Remco Energy"


SUPPORTED_BRANDS: set[SupportedBrand] = {
    SupportedBrand.VICTRON,
    SupportedBrand.REMCO,
}
