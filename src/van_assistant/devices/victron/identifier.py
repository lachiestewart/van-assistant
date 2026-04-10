import struct

from van_assistant.devices.base.identifier import DeviceIdentifier
from van_assistant.devices.victron.devices.ac_charger import VictronACCharger
from van_assistant.devices.victron.devices.base import VictronDevice
from van_assistant.devices.victron.devices.battery_monitor import VictronBatteryMonitor
from van_assistant.devices.victron.devices.battery_sense import VictronBatterySense
from van_assistant.devices.victron.devices.dc_energy_meter import VictronDCEnergyMeter
from van_assistant.devices.victron.devices.dcdc_converter import VictronDCDCConverter
from van_assistant.devices.victron.devices.inverter import VictronInverter
from van_assistant.devices.victron.devices.lynx_smart_bms import VictronLynxSmartBMS
from van_assistant.devices.victron.devices.multirs import VictronMultiRS
from van_assistant.devices.victron.devices.orion_xs import VictronOrionXS
from van_assistant.devices.victron.devices.smart_battery_protect import (
    VictronSmartBatteryProtect,
)
from van_assistant.devices.victron.devices.smart_lithium import VictronSmartLithium
from van_assistant.devices.victron.devices.solar_charger import VictronSolarCharger
from van_assistant.devices.victron.devices.vebus import VictronVEBus

# Add to this list if a device should be forced to use a particular implementation
# instead of relying on the identifier in the advertisement
MODEL_PARSER_OVERRIDE: dict[int, type[VictronDevice]] = {
    0xA3A4: VictronBatterySense,  # Smart Battery Sense
    0xA3A5: VictronBatterySense,  # Smart Battery Sense
}

MODE_DEVICE_MAP: dict[int, type[VictronDevice]] = {
    0x2: VictronBatteryMonitor,
    0xD: VictronDCEnergyMeter,
    0x8: VictronACCharger,
    0x4: VictronDCDCConverter,
    0x3: VictronInverter,
    # 0x6: InverterRS (not implemented)
    0xA: VictronLynxSmartBMS,
    0xB: VictronMultiRS,
    0x5: VictronSmartLithium,
    0x9: VictronSmartBatteryProtect,
    0x1: VictronSolarCharger,
    0xC: VictronVEBus,
    0xF: VictronOrionXS,
}


class VictronDeviceIdentifier(DeviceIdentifier):
    """Device identifier for Victron devices.

    Uses the model ID and mode from the advertisement to determine the device type.
    """

    @staticmethod
    def detect_device_type(data: bytes) -> type[VictronDevice] | None:
        """Detect the device type from the advertisement data.

        Args:
            data: The advertisement data.

        Returns:
            The device type if it can be determined, otherwise None.

        """
        try:
            model_id, mode = struct.unpack_from("<HB", data, 2)
        except IndexError:
            return None

        # Model ID override takes priority
        if model_id in MODEL_PARSER_OVERRIDE:
            return MODEL_PARSER_OVERRIDE[model_id]

        return MODE_DEVICE_MAP.get(mode)
