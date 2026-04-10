from enum import Enum

from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import (
    ACInState,
    BitReader,
    OperationMode,
)


class AlarmNotification(Enum):
    """Enum of alarm notifications."""

    NO_ALARM = 0
    WARNING = 1
    ALARM = 2
    UNKNOWN = 3


class VictronVEBusData(DeviceData):
    """Structured data for Victron VE.Bus devices."""

    def get_device_state(self) -> OperationMode | None:
        """Return an enum indicating the device state."""
        return self.data.get("device_state")

    def get_error(self) -> int | None:
        """Return the VEBus error state (unknown interpretation)."""
        return self.data.get("error")

    def get_alarm(self) -> AlarmNotification | None:
        """Return the VEBus alarm state."""
        return self.data.get("alarm")

    def get_ac_in_state(self) -> ACInState | None:
        """Return an enum indicating the current ac power state."""
        return self.data.get("ac_in_state")

    def get_ac_in_power(self) -> float | None:
        """Return the current AC power draw."""
        return self.data.get("ac_in_power")

    def get_ac_out_power(self) -> float | None:
        """Return the current AC power output."""
        return self.data.get("ac_out_power")

    def get_battery_current(self) -> float | None:
        """Return the battery current in amps (positive for charging, negative for inverting)."""
        return self.data.get("battery_current")

    def get_battery_voltage(self) -> float | None:
        """Return the battery voltage in volts."""
        return self.data.get("battery_voltage")

    def get_battery_temperature(self) -> float | None:
        """Return the battery temperature in degrees celcius."""
        return self.data.get("battery_temperature")

    def get_soc(self) -> float | None:
        """Return the battery state of charge as a percentage."""
        return self.data.get("soc")


class VictronVEBus(VictronDevice):
    """Device class for Victron VE.Bus devices, which provide data via BLE advertisements."""

    data_type = VictronVEBusData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        # Device state
        device_state = reader.read_unsigned_int(8)
        # VE.Bus error (docs do not explain how to interpret)
        error = reader.read_unsigned_int(8)
        # Battery charging Current reading in 0.1A increments
        battery_current = reader.read_signed_int(16)
        # Battery voltage reading in 0.01V increments (14 bits)
        # Active AC in state (enum) (2 bits)
        battery_voltage = reader.read_unsigned_int(14)
        # AC input active
        ac_in_state = reader.read_unsigned_int(2)
        # Active AC in power in 1W increments (19 bits, signed)
        ac_in_power = reader.read_signed_int(19)
        # AC out power in 1W increments (19 bits, signed)
        ac_out_power = reader.read_signed_int(19)
        # Alarm (enum but docs say "to be defined") (2 bits)
        alarm = reader.read_unsigned_int(2)
        # Battery temperature in 1 degree celcius increments (7 bits)
        battery_temperature = reader.read_unsigned_int(7)
        # Battery state of charge in 1% increments (7 bits)
        soc = reader.read_unsigned_int(7)

        return {
            "device_state": OperationMode(device_state),
            "error": error if error != 0xFF else None,
            "battery_voltage": (battery_voltage / 100 if battery_voltage != 0x3FFF else None),
            "battery_current": (battery_current / 10 if battery_current != 0x7FFF else None),
            "ac_in_state": ACInState(ac_in_state),
            "ac_in_power": ac_in_power if ac_in_power != 0x3FFFF else None,
            "ac_out_power": ac_out_power if ac_out_power != 0x3FFFF else None,
            "alarm": AlarmNotification(alarm),
            "battery_temperature": (
                battery_temperature - 40 if battery_temperature != 0x7F else None
            ),
            "soc": soc if soc != 0x7F else None,
        }
