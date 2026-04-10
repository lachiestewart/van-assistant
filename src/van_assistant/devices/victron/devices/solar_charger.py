from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import BitReader, ChargerError, OperationMode


class VictronSolarChargerData(DeviceData):
    """Structured data class for Victron Solar Charger data."""

    def get_charge_state(self) -> OperationMode | None:
        """Return an enum indicating the current charging state."""
        return self.data.get("charge_state")

    def get_charger_error(self) -> ChargerError | None:
        """Return an enum indicating the current charging error."""
        return self.data.get("charger_error")

    def get_battery_voltage(self) -> float | None:
        """Return the battery voltage in volts."""
        return self.data.get("battery_voltage")

    def get_battery_charging_current(self) -> float | None:
        """Return the battery charging current in amps."""
        return self.data.get("battery_charging_current")

    def get_yield_today(self) -> float | None:
        """Return the yield_today in Wh."""
        return self.data.get("yield_today")

    def get_solar_power(self) -> float | None:
        """Return the current solar power in W."""
        return self.data.get("solar_power")

    def get_external_device_load(self) -> float | None:
        """Return the external device load in amps."""
        return self.data.get("external_device_load")


class VictronSolarCharger(VictronDevice):
    """Device class for Victron solar chargers."""

    data_type = VictronSolarChargerData

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
        # Battery voltage reading in 0.01V increments
        battery_voltage = reader.read_signed_int(16)
        # Battery charging Current reading in 0.1A increments
        battery_charging_current = reader.read_signed_int(16)
        # Todays solar power yield in 10Wh increments
        yield_today = reader.read_unsigned_int(16)
        # Current power from solar in 1W increments
        solar_power = reader.read_unsigned_int(16)
        # External device load in 0.1A increments
        external_device_load = reader.read_unsigned_int(9)

        return {
            "charge_state": OperationMode(charge_state),
            "charger_error": ChargerError(0 if charger_error == 0xFF else charger_error),
            "battery_voltage": (battery_voltage / 100 if battery_voltage != 0x7FFF else None),
            "battery_charging_current": (
                battery_charging_current / 10 if battery_charging_current != 0x7FFF else None
            ),
            "yield_today": yield_today * 10 if yield_today != 0xFFFF else None,
            "solar_power": solar_power if solar_power != 0xFFFF else None,
            "external_device_load": (
                external_device_load / 10 if external_device_load != 0x1FF else None
            ),
        }
