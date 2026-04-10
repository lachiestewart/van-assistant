from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import AlarmReason, BitReader, OperationMode


class VictronInverterData(DeviceData):
    """Structured data class for Victron Inverter data."""

    def get_device_state(self) -> OperationMode | None:
        """Return an enum indicating the current device state."""
        return self.data.get("device_state")

    def get_alarm(self) -> AlarmReason | None:
        """Return an enum indicating the current alarm reason or None otherwise."""
        return self.data.get("alarm")

    def get_battery_voltage(self) -> float | None:
        """Return the battery voltage in volts."""
        return self.data.get("battery_voltage")

    def get_ac_apparent_power(self) -> int | None:
        """Return the output AC power in voltampere."""
        return self.data.get("ac_apparent_power")

    def get_ac_voltage(self) -> float | None:
        """Return the output AC voltage in volts."""
        return self.data.get("ac_voltage")

    def get_ac_current(self) -> float | None:
        """Return the output AC current in amperes."""
        return self.data.get("ac_current")


class VictronInverter(VictronDevice):
    """Class representing a Victron Inverter device."""

    data_type = VictronInverterData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        # Device State:   0 - Off
        device_state = reader.read_unsigned_int(8)
        # Alarm Reason Code
        alarm = reader.read_unsigned_int(16)
        # Input voltage reading in 0.01V increments
        battery_voltage = reader.read_signed_int(16)
        # Output AC power in 1VA
        ac_apparent_power = reader.read_unsigned_int(16)
        # Output AC voltage in 0.01V
        ac_voltage = reader.read_unsigned_int(15)
        # Output AC current in 0.1A
        ac_current = reader.read_unsigned_int(11)

        return {
            "device_state": OperationMode(device_state),
            "alarm": AlarmReason(alarm),
            "battery_voltage": ((battery_voltage) / 100 if battery_voltage != 0x7FFF else None),
            "ac_apparent_power": (ac_apparent_power if ac_apparent_power != 0xFFFF else None),
            "ac_voltage": ac_voltage / 100 if ac_voltage != 0x7FFF else None,
            "ac_current": ac_current / 10 if ac_current != 0x7FF else None,
        }
