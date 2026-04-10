import asyncio

from van_assistant.devices.remco.devices.bms import RemcoBattery
from van_assistant.notification_services.logging_service import LoggingService


async def test_bms() -> None:
    address = "A5:C2:37:63:34:61"
    not_ser = LoggingService()
    device = RemcoBattery(address, not_ser)

    device_task = asyncio.create_task(device.start())
    await asyncio.sleep(30)
    await device.stop()
    await device_task


def main() -> None:
    asyncio.run(test_bms())


if __name__ == "__main__":
    main()
