import asyncio
import struct
from datetime import date
from itertools import cycle

from bleak.backends.characteristic import BleakGATTCharacteristic

from van_assistant.devices.base.ble_connect_device import BLEConnectableDevice
from van_assistant.notification_services.base import NotificationService
from van_assistant.notification_services.logging_service import LoggingService

NOTIFY_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

CMD_INFO = bytes.fromhex("dd a5 03 00 ff fd 77")
CMD_CELL = bytes.fromhex("dd a5 04 00 ff fc 77")

PACKET_HEADER = 0xDD
PACKET_TAIL = 0x77
BATT_INFO = 0x03
CELL_INFO = 0x04


POLL_INTERVAL = 5.0


class RemcoDevice(BLEConnectableDevice):

    def __init__(self, addr: str, notification_service: NotificationService) -> None:
        super().__init__(addr, notification_service)

        self._command_buffer: bytearray = bytearray()

        self.commands = [CMD_INFO, CMD_CELL]

    def _get_notify_uuid(self) -> str:
        return NOTIFY_UUID

    async def _run(self) -> None:
        for cmd in cycle(self.commands):
            if not self._running:
                break

            await self._send(cmd)
            await asyncio.sleep(POLL_INTERVAL)

    async def _send(self, pkt: bytes) -> None:
        if not self._client:
            return

        await self._client.write_gatt_char(
            WRITE_UUID,
            pkt,
            response=False,
        )

    async def _notify_handler(
        self,
        sender: BleakGATTCharacteristic,
        data: bytearray,
    ) -> None:

        self._command_buffer.extend(data)

        if len(self._command_buffer) == 0:
            return

        if self._command_buffer[0] != PACKET_HEADER:
            self._command_buffer.clear()
            return

        if self._command_buffer[-1] == PACKET_TAIL:
            self._process_buffer(self._command_buffer.copy())
            self._command_buffer.clear()

    def _process_buffer(self, buffer: bytearray) -> None:
        cmd = buffer[1]

        data_buffer = buffer[4:-1]

        if cmd == BATT_INFO:
            self._decode_info(data_buffer)
            return

        if cmd == CELL_INFO:
            self._decode_cells(data_buffer)

    def _decode_info(self, data: bytearray) -> None:

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
        ) = struct.unpack_from(">HhHHHHHHHBBBBBHH", data)

        data_res: dict[str, float | str | list[float]] = {}

        volts /= 100
        amps /= 100
        capacity /= 100
        remain /= 100
        temps = [temp1, temp2]
        temps = temps[:sensors]
        temps = [(temp - 2731) / 10 for temp in temps]

        mdate = self._parse_manufacture_date(mdate)

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

    def _decode_cells(self, data: bytearray):

        cell_count = (len(data) - 2) // 2

        cells = struct.unpack_from(
            f">{cell_count}H",
            data,
        )

        cells = [cell / 1000 for cell in cells]

        for i, cell in enumerate(cells):
            self.notification_service.publish(f"bms/cell_voltages/{i}", cell)


    def _parse_manufacture_date(self, mdate: int) -> str:
        year  = ((mdate >> 9) & 0x7F) + 2000
        month = (mdate >> 5) & 0x0F
        day   = mdate & 0x1F
        return str(date(year, month, day))

async def main():

    address = "A5:C2:37:63:34:61"
    not_ser = LoggingService()
    device = RemcoDevice(address, not_ser)

    start_task = asyncio.create_task(device.start())
    await asyncio.sleep(30)
    await device.stop()
    await start_task


if __name__ == "__main__":
    asyncio.run(main())
