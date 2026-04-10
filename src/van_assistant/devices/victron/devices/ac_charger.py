from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import BitReader, ChargerError, OperationMode


class VictronACChargerData(DeviceData):
    """Structured data class for Victron AC Charger data."""

    def get_charge_state(self) -> OperationMode | None:
        """Return an enum indicating the current charging state."""
        return self.data.get("charge_state")

    def get_charger_error(self) -> ChargerError | None:
        """Return an enum indicating the current charging error."""
        return self.data.get("charger_error")

    def get_output_voltage1(self) -> float | None:
        """Return the output voltage in volts."""
        return self.data.get("output_voltage1")

    def get_output_voltage2(self) -> float | None:
        """Return the output voltage in volts."""
        return self.data.get("output_voltage2")

    def get_output_voltage3(self) -> float | None:
        """Return the output voltage in volts."""
        return self.data.get("output_voltage3")

    def get_output_current1(self) -> float | None:
        """Return the output charging current in amps."""
        return self.data.get("output_current1")

    def get_output_current2(self) -> float | None:
        """Return the output charging current in amps."""
        return self.data.get("output_current2")

    def get_output_current3(self) -> float | None:
        """Return the output charging current in amps."""
        return self.data.get("output_current3")

    def get_temperature(self) -> float | None:
        """Return the temperature of the charger in celcius."""
        return self.data.get("temperature")

    def get_ac_current(self) -> float | None:
        """Return the input current in amps."""
        return self.data.get("ac_current")


class VictronACCharger(VictronDevice):
    """Class representing a Victron AC Charger device."""

    data_type = VictronACChargerData

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
        charge_state = reader.read_unsigned_int(8)
        charger_error = reader.read_unsigned_int(8)
        output_voltage1 = reader.read_unsigned_int(
            13,
        )  # Output voltage reading in 0.01V increments
        output_current1 = reader.read_unsigned_int(
            11,
        )  # Output current reading in 0.1A increments
        output_voltage2 = reader.read_unsigned_int(13)
        output_current2 = reader.read_unsigned_int(11)
        output_voltage3 = reader.read_unsigned_int(13)
        output_current3 = reader.read_unsigned_int(11)
        temperature = reader.read_unsigned_int(7)  # Celsius
        ac_current = reader.read_unsigned_int(
            9,
        )  # AC current reading in 0.1A increments

        return {
            "charge_state": OperationMode(charge_state),
            "charger_error": ChargerError(0 if charger_error == 0xFF else charger_error),
            "output_voltage1": (output_voltage1 / 100 if output_voltage1 != 0x1FFF else None),
            "output_voltage2": (output_voltage2 / 100 if output_voltage2 != 0x1FFF else None),
            "output_voltage3": (output_voltage3 / 100 if output_voltage3 != 0x1FFF else None),
            "output_current1": (output_current1 / 10 if output_current1 != 0x7FF else None),
            "output_current2": (output_current2 / 10 if output_current2 != 0x7FF else None),
            "output_current3": (output_current3 / 10 if output_current3 != 0x7FF else None),
            "temperature": ((temperature - 40) if temperature != 0x7F else None),
            "ac_current": (ac_current / 10 if ac_current != 0x1FF else None),
        }
