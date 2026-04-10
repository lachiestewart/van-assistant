from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import (
    AlarmReason,
    AuxMode,
    BitReader,
    kelvin_to_celsius,
)


class VictronBatteryMonitorData(DeviceData):
    """Structured data class for Victron Battery Monitor data."""

    def get_remaining_mins(self) -> float | None:
        """Return the number of remaining minutes of battery life in minutes."""
        return self.data.get("remaining_mins")

    def get_current(self) -> float | None:
        """Return the current in amps."""
        return self.data.get("current")

    def get_voltage(self) -> float | None:
        """Return the voltage in volts."""
        return self.data.get("voltage")

    def get_soc(self) -> float | None:
        """Return the state of charge in percentage."""
        return self.data.get("soc")

    def get_consumed_ah(self) -> float | None:
        """Return the consumed energy in amp hours."""
        return self.data.get("consumed_ah")

    def get_alarm(self) -> AlarmReason:
        """Return an enum indicating the current alarm reason."""
        return self.data.get("alarm")

    def get_aux_mode(self) -> AuxMode:
        """Return an enum indicating the current auxiliary input mode."""
        return self.data.get("aux_mode")

    def get_temperature(self) -> float | None:
        """Return the temperature in Celsius if the aux input is set to temperature."""
        return self.data.get("temperature")

    def get_starter_voltage(self) -> float | None:
        """Return the starter battery voltage in volts if the aux input is set to starter battery."""
        return self.data.get("starter_voltage")

    def get_midpoint_voltage(self) -> float | None:
        """Return the midpoint battery voltage in volts if the aux input is set to midpoint voltage."""
        return self.data.get("midpoint_voltage")


class VictronBatteryMonitor(VictronDevice):
    """Class representing a Victron Battery Monitor device."""

    data_type: type[DeviceData] = VictronBatteryMonitorData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        # Remaining time in minutes
        remaining_mins = reader.read_unsigned_int(16)
        # Voltage reading in 10mV increments
        voltage = reader.read_signed_int(16)
        # Alarm reason
        alarm = reader.read_unsigned_int(16)
        # Value of the auxillary input (millivolts or degrees)
        aux = reader.read_unsigned_int(16)
        aux_mode = reader.read_unsigned_int(2)
        # The current in milliamps
        current = reader.read_signed_int(22)
        # Consumed Ah in 0.1Ah increments
        consumed_ah = reader.read_unsigned_int(20)
        # The state of charge in 0.1% increments
        soc = reader.read_unsigned_int(10)

        parsed = {
            "remaining_mins": remaining_mins if remaining_mins != 0xFFFF else None,
            "voltage": voltage / 100 if voltage != 0x7FFF else None,
            "alarm": AlarmReason(alarm),
            "aux_mode": AuxMode(aux_mode),
            "current": current / 1000 if current != 0x3FFFFF else None,
            "consumed_ah": -consumed_ah / 10 if consumed_ah != 0xFFFFF else None,
            "soc": soc / 10 if soc != 0x3FF else None,
        }

        if aux_mode == AuxMode.STARTER_VOLTAGE.value:
            # Starter voltage is treated as signed
            parsed["starter_voltage"] = BitReader.to_signed_int(aux, 16) / 100
        elif aux_mode == AuxMode.MIDPOINT_VOLTAGE.value:
            parsed["midpoint_voltage"] = aux / 100
        elif aux_mode == AuxMode.TEMPERATURE.value:
            temperature_kelvin = aux / 100
            temperature_celsius = kelvin_to_celsius(temperature_kelvin)
            parsed["temperature"] = temperature_celsius

        return parsed
