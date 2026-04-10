from enum import Enum

from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import (
    AlarmReason,
    AuxMode,
    BitReader,
    kelvin_to_celsius,
)


class MeterType(Enum):
    """Enum representing the type of a Victron DC Energy Meter."""

    SOLAR_CHARGER = -9
    WIND_CHARGER = -8
    SHAFT_GENERATOR = -7
    ALTERNATOR = -6
    FUEL_CELL = -5
    WATER_GENERATOR = -4
    DC_DC_CHARGER = -3
    AC_CHARGER = -2
    GENERIC_SOURCE = -1
    GENERIC_LOAD = 1
    ELECTRIC_DRIVE = 2
    FRIDGE = 3
    WATER_PUMP = 4
    BILGE_PUMP = 5
    DC_SYSTEM = 6
    INVERTER = 7
    WATER_HEATER = 8


class VictronDCEnergyMeterData(DeviceData):
    """Structured data class for Victron DC Energy Meter data."""

    def get_meter_type(self) -> MeterType:
        """Return an enum indicating the current meter type."""
        return self.data.get("meter_type")

    def get_current(self) -> float | None:
        """Return the current in amps."""
        return self.data.get("current")

    def get_voltage(self) -> float | None:
        """Return the voltage in volts."""
        return self.data.get("voltage")

    def get_alarm(self) -> AlarmReason | None:
        """Return an enum indicating the current alarm reason or None otherwise."""
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


class VictronDCEnergyMeter(VictronDevice):
    """Class representing a Victron DC Energy Meter device."""

    data_type = VictronDCEnergyMeterData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)

        meter_type = reader.read_signed_int(16)
        # Voltage reading in 10mV increments
        voltage = reader.read_signed_int(16)
        # Alarm reason
        alarm_int = reader.read_unsigned_int(16)
        # Value of the auxillary input
        aux = reader.read_unsigned_int(16)
        # The aux input mode:
        #   0 = Starter battery voltage
        #   2 = Temperature
        #   3 = Disabled
        aux_mode = reader.read_unsigned_int(2)
        # The current in milliamps
        current = reader.read_signed_int(22)

        parsed = {
            "meter_type": MeterType(meter_type),
            "aux_mode": AuxMode(aux_mode),
            "current": current / 1000 if current != 0x3FFFFF else None,
            "voltage": voltage / 100 if voltage != 0x7FFF else None,
            "alarm": AlarmReason(alarm_int),
        }

        if aux_mode == AuxMode.STARTER_VOLTAGE.value:
            # Starter voltage is treated as signed
            parsed["starter_voltage"] = BitReader.to_signed_int(aux, 16) / 100

        elif aux_mode == AuxMode.TEMPERATURE.value and aux != 0xFFFF:
            temperature_kelvin = aux / 100
            temperature_celsius = kelvin_to_celsius(temperature_kelvin)
            parsed["temperature"] = temperature_celsius

        return parsed
