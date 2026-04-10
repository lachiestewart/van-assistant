import struct
from enum import Enum

from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import ACInState, ChargerError


class MultiRSOperationMode(Enum):
    """Enum representing the operation mode of a MultiRS device."""

    OFF = 0
    LOW_POWER = 1
    FAULT = 2
    BULK = 3
    ABSORPTION = 4
    FLOAT = 5
    STORAGE = 6
    EQUALIZE_MANUAL = 7
    PASSTHRU = 8
    INVERTING = 9
    ASSISTING = 10
    POWER_SUPPLY = 11
    SUSTAIN = 244
    STARTING_UP = 245
    REPEATED_ABSORPTION = 246
    AUTO_EQUALIZE = 247
    BATTERY_SAFE = 248
    LOAD_DETECT = 249
    BLOCKED = 250
    TEST = 251
    EXTERNAL_CONTROL = 252
    NOT_AVAILABLE = 255


class VictronMultiRSData(DeviceData):
    """Class holding parsed data from a MultiRS device."""

    def get_device_state(self) -> MultiRSOperationMode | None:
        """Return an enum indicating the current device state."""
        return self.data.get("device_state")

    def get_charger_error(self) -> ChargerError | None:
        """Return an enum indicating the current charging error."""
        return self.data.get("charger_error")

    def get_battery_voltage(self) -> float | None:
        """Return the battery voltage in volts."""
        return self.data.get("battery_voltage")

    def get_battery_current(self) -> float | None:
        """Return the battery current in amperes."""
        return self.data.get("battery_current")

    def get_yield_today(self) -> float | None:
        """Return the yield today in kWh."""
        return self.data.get("yield_today")

    def get_pv_power(self) -> int | None:
        """Return the PV power in watts."""
        return self.data.get("pv_power")

    def get_active_ac_in_power(self) -> int | None:
        """Return the active AC in power in watts."""
        return self.data.get("active_ac_in_power")

    def get_active_ac_out_power(self) -> int | None:
        """Return the active AC out power in watts."""
        return self.data.get("active_ac_out_power")

    def get_active_ac_in(self) -> ACInState | None:
        """Return an enum indicating the active AC in."""
        return self.data.get("active_ac_in")


class VictronMultiRS(VictronDevice):
    """A class representing a MultiRS device."""

    data_type = VictronMultiRSData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        (
            device_state,
            charger_error,
            battery_current,
            battery_voltage_ac_in,
            active_ac_in_power,
            active_ac_out_power,
            pv_power,
            yield_today,
        ) = struct.unpack("<bbhHhhHH", decrypted[:14])

        battery_voltage = (battery_voltage_ac_in & 0x3FFF) / 100.0
        active_ac_in = (battery_voltage_ac_in >> 14) & 0x03

        return {
            "device_state": MultiRSOperationMode(device_state),
            "charger_error": ChargerError(0 if charger_error == 0xFF else charger_error),
            "battery_current": (battery_current / 10.0 if battery_current != 0x7FFF else None),
            "battery_voltage": battery_voltage,
            "active_ac_in": ACInState(active_ac_in),
            "active_ac_in_power": (active_ac_in_power if active_ac_in_power != 0x7FFF else None),
            "active_ac_out_power": (active_ac_out_power if active_ac_out_power != 0x7FFF else None),
            "pv_power": pv_power if pv_power != 0xFFFF else None,
            "yield_today": yield_today / 100.0 if yield_today != 0xFFFF else None,
        }
