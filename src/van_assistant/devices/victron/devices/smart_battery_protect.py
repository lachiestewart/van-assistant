from enum import Enum

from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import (
    AlarmReason,
    BitReader,
    ChargerError,
    OffReason,
    OperationMode,
)


class OutputState(Enum):
    """Enum representing the output state of a Smart Battery Protect device."""

    SHUTDOWN = 0
    ON = 1
    OFF = 4
    UNKNOWN = 255


class VictronSmartBatteryProtectData(DeviceData):
    """Structured data class for Victron Smart Battery Protect data."""

    def get_device_state(self) -> OperationMode | None:
        """Return the device state."""
        return self.data.get("device_state")

    def get_output_state(self) -> OutputState | None:
        """Return the output state."""
        return self.data.get("output_state")

    def get_charger_error(self) -> ChargerError | None:
        """Return the charger error."""
        return self.data.get("charger_error")

    def get_alarm_reason(self) -> AlarmReason:
        """Return the alarm reason."""
        return self.data.get("alarm_reason")

    def get_warning_reason(self) -> AlarmReason:
        """Return the warning reason."""
        return self.data.get("warning_reason")

    def get_input_voltage(self) -> float | None:
        """Return the input voltage in volts."""
        return self.data.get("input_voltage")

    def get_output_voltage(self) -> float | None:
        """Return the output voltage in volts."""
        return self.data.get("output_voltage")

    def get_off_reason(self) -> OffReason:
        """Return the off reason."""
        return self.data.get("off_reason")


class VictronSmartBatteryProtect(VictronDevice):
    """Class representing a Victron Smart Battery Protect device."""

    data_type = VictronSmartBatteryProtectData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        device_state = reader.read_unsigned_int(8)
        output_state = reader.read_unsigned_int(8)
        charger_error = reader.read_unsigned_int(8)
        alarm_reason = reader.read_unsigned_int(16)
        warning_reason = reader.read_unsigned_int(16)
        input_voltage = reader.read_signed_int(16)
        output_voltage = reader.read_unsigned_int(16)
        off_reason = reader.read_unsigned_int(32)

        return {
            "device_state": OperationMode(device_state),
            "output_state": OutputState(output_state),
            "charger_error": ChargerError(0 if charger_error == 0xFF else charger_error),
            "alarm_reason": AlarmReason(alarm_reason),
            "warning_reason": AlarmReason(warning_reason),
            "input_voltage": (input_voltage / 100 if input_voltage != 0x7FFF else None),
            "output_voltage": (output_voltage / 100 if output_voltage != 0xFFFF else None),
            "off_reason": OffReason(off_reason),
        }
