from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import (
    BitReader,
    ChargerError,
    OffReason,
    OperationMode,
)


class VictronDCDCConverterData(DeviceData):
    """Structured data class for Victron DC-DC Converter data."""

    def get_charge_state(self) -> OperationMode | None:
        """Return an enum indicating the current charging state."""
        return self.data.get("device_state")

    def get_charger_error(self) -> ChargerError | None:
        """Return an enum indicating the error code."""
        return self.data.get("charger_error")

    def get_input_voltage(self) -> float | None:
        """Return the input voltage in volts."""
        return self.data.get("input_voltage")

    def get_output_voltage(self) -> float | None:
        """Return the output voltage in volts."""
        return self.data.get("output_voltage")

    def get_off_reason(self) -> OffReason:
        """Return an error code stating the reason for the output to be off."""
        return self.data.get("off_reason")


class VictronDCDCConverter(VictronDevice):
    """Class representing a Victron DC-DC Converter device."""

    data_type = VictronDCDCConverterData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        # Charge State:   0 - Off
        #                 3 - Bulk
        #                 4 - Absorption
        #                 5 - Float
        device_state = reader.read_unsigned_int(8)
        # Charger Error Code
        charger_error = reader.read_unsigned_int(8)
        # Input voltage reading in 0.01V increments
        input_voltage = reader.read_unsigned_int(16)
        # Output voltage in 0.01V
        output_voltage = reader.read_signed_int(16)
        # Reason for Charger Off
        off_reason = reader.read_unsigned_int(32)

        return {
            "device_state": OperationMode(device_state),
            "charger_error": ChargerError(0 if charger_error == 0xFF else charger_error),
            "input_voltage": input_voltage / 100 if input_voltage != 0xFFFF else None,
            "output_voltage": (output_voltage / 100 if output_voltage != 0x7FFF else None),
            "off_reason": OffReason(off_reason),
        }
