import struct
from datetime import date

from van_assistant.devices.remco.devices.base import RemcoDevice

CMD_INFO = bytes.fromhex("dd a5 03 00 ff fd 77")
CMD_CELL = bytes.fromhex("dd a5 04 00 ff fc 77")

BATT_INFO = 0x03
CELL_INFO = 0x04


class RemcoBattery(RemcoDevice):
    """Remco battery device."""

    def get_commands(self) -> list[bytes]:
        """Return the list of commands to poll from the device."""
        return [CMD_INFO, CMD_CELL]

    def parse(self, packet: bytearray) -> None:
        """Parse a complete packet from the device.

        Args:
            packet: The complete packet data to parse.

        """
        cmd = packet[1]

        data_buffer = packet[4:-1]

        if cmd == BATT_INFO:
            self.decode_info(data_buffer)
            return

        if cmd == CELL_INFO:
            self.decode_cells(data_buffer)

    def decode_info(self, packet_data: bytearray) -> None:
        """Decode the battery information from the data buffer.

        Args:
            packet_data: The data buffer containing the battery information.

        """
        (
            volts,
            amps,
            remain,
            capacity,
            cycles,
            mdate,
            balance1,
            balance2,
            protect,
            vers,
            percent,
            fet,
            cells,
            sensors,
            temp1,
            temp2,
        ) = struct.unpack_from(">HhHHHHHHHBBBBBHH", packet_data)

        data_res: dict[str, float | str | list[float]] = {}

        volts /= 100
        amps /= 100
        capacity /= 100
        remain /= 100
        temps = [temp1, temp2]
        temps = temps[:sensors]
        temps = [(temp - 2731) / 10 for temp in temps]

        mdate = self.parse_manufacture_date(mdate)

        data_res["volts"] = volts
        data_res["amps"] = amps
        data_res["remain"] = remain
        data_res["capacity"] = capacity
        data_res["cycles"] = cycles
        data_res["mdate"] = mdate
        data_res["balance1"] = balance1
        data_res["balance2"] = balance2
        data_res["protect"] = protect
        data_res["vers"] = vers
        data_res["percent"] = percent
        data_res["fet"] = fet
        data_res["cells"] = cells
        data_res["temps"] = temps

        for key, val in data_res.items():
            if isinstance(val, list):
                for i, list_val in enumerate(val):
                    self.notification_service.publish(f"bms/{key}/{i}", list_val)
            else:
                self.notification_service.publish(f"bms/{key}", val)

    def decode_cells(self, packet_data: bytearray) -> None:
        """Decode the individual cell voltages from the data buffer.

        Args:
            packet_data: The data buffer containing the cell voltage information.

        """
        cell_count = (len(packet_data) - 2) // 2

        cells = struct.unpack_from(
            f">{cell_count}H",
            packet_data,
        )

        cells = [cell / 1000 for cell in cells]

        for i, cell in enumerate(cells):
            self.notification_service.publish(f"bms/cell_voltages/{i}", cell)

    def parse_manufacture_date(self, mdate: int) -> str:
        """Parse the manufacture date from the raw integer value.

        Args:
            mdate: The raw integer value representing the manufacture date.

        Returns:
            A string representation of the manufacture date in the format "YYYY-MM-DD".

        """
        year = ((mdate >> 9) & 0x7F) + 2000
        month = (mdate >> 5) & 0x0F
        day = mdate & 0x1F
        return str(date(year, month, day))
