from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.battery_monitor import VictronBatteryMonitor


class VictronBatterySenseData(DeviceData):
    """Structured data class for Victron Battery Sense data."""

    def get_temperature(self) -> float:
        """Return the temperature in Celsius."""
        return self.data.get("temperature")

    def get_voltage(self) -> float | None:
        """Return the voltage in volts."""
        return self.data.get("voltage")


class VictronBatterySense(VictronBatteryMonitor):
    """Class representing a Victron Battery Sense device."""

    data_type = VictronBatterySenseData
