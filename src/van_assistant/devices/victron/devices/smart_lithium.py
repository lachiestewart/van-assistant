from enum import Enum

from van_assistant.devices.base.device_data import DeviceData
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.utils import BitReader


class BalancerStatus(Enum):
    """Enum representing the balancer status of a Smart Lithium device."""

    UNKNOWN = 0
    BALANCED = 1
    BALANCING = 2
    IMBALANCE = 3


class VictronSmartLithiumData(DeviceData):
    """Structured data class for Victron Smart Lithium data."""

    def get_bms_flags(self) -> int:
        """Get the raw bms_flags field (meaning not documented)."""
        return self.data.get("bms_flags")

    def get_error_flags(self) -> int:
        """Get the raw error_flags field (meaning not documented)."""
        return self.data.get("error_flags")

    def get_battery_voltage(self) -> float | None:
        """Return the voltage in volts."""
        return self.data.get("battery_voltage")

    def get_battery_temperature(self) -> int | None:
        """Return the temperature in Celsius if the aux input is set to temperature."""
        return self.data.get("battery_temperature")

    def get_cell_voltages(self) -> list:
        """Return the voltage of each cell (floats where -inf is <2.61V, +inf is >3.85V, None is N/A)."""
        return self.data.get("cell_voltages")

    def get_balancer_status(self) -> BalancerStatus | None:
        """Get the raw balancer_status field (meaning not documented)."""
        return self.data.get("balancer_status")


class VictronSmartLithium(VictronDevice):
    """Class representing a Victron Smart Lithium device."""

    data_type = VictronSmartLithiumData

    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
        reader = BitReader(decrypted)
        bms_flags = reader.read_unsigned_int(32)
        error_flags = reader.read_unsigned_int(16)
        cell_voltages = [reader.read_unsigned_int(7) for _ in range(8)]
        battery_voltage = reader.read_unsigned_int(12)
        balancer_status = reader.read_unsigned_int(4)
        battery_temperature = reader.read_unsigned_int(7)

        return {
            "bms_flags": bms_flags,
            "error_flags": error_flags,
            "cell_voltages": [parse_cell_voltage(v) for v in cell_voltages],
            "battery_voltage": (battery_voltage / 100.0 if battery_voltage != 0x0FFF else None),
            "balancer_status": BalancerStatus(0 if balancer_status == 0xF else balancer_status),
            "battery_temperature": (
                (battery_temperature - 40) if battery_temperature != 0x7F else None
            ),  # Celsius
        }


def parse_cell_voltage(payload: int) -> float | None:
    """Parse a cell voltage payload into a voltage in volts.

    Args:
        payload: The raw cell voltage payload (0-127).

    Returns:
        The cell voltage in volts, or None if the voltage is not available.

    """
    return {0x00: float("-inf"), 0x7E: float("inf"), 0x7F: None}.get(
        payload,
        (260 + payload) / 100.0,
    )
