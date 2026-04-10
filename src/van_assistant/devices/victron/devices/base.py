import logging
import struct
from abc import abstractmethod

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad

from van_assistant.devices.base.ble_ad_device import BLEAdvertisementDevice
from van_assistant.devices.base.device_data import DeviceData

logger = logging.getLogger(__name__)


class VictronDevice(BLEAdvertisementDevice):
    """Base class for Victron devices."""

    data_type: type[DeviceData] = DeviceData
    connectable = False

    async def handle_data(self, data: bytes | bytearray) -> None:
        """Handle incoming data from the device."""
        if not self.encryption_key or isinstance(data, bytearray):
            return

        fmt = "<HHBH"
        size = struct.calcsize(fmt)

        _, model_id, _, iv = struct.unpack_from(fmt, data)
        encrypted_data = data[size:]

        encryption_key = bytes.fromhex(self.encryption_key)

        if encrypted_data[0] != encryption_key[0]:
            logger.warning(
                f"Skipping packet with invalid encryption key prefix: {encrypted_data[0]}",
            )
            return

        ctr = Counter.new(128, initial_value=iv, little_endian=True)

        cipher = AES.new(
            encryption_key,
            AES.MODE_CTR,
            counter=ctr,
        )

        decrypted_data = cipher.decrypt(pad(encrypted_data[1:], 16))

        parsed_data = self.parse(decrypted_data)
        parsed_data["model_id"] = model_id

        device_data = self.data_type(parsed_data)

        logger.info(device_data)

    @abstractmethod
    def parse(self, decrypted: bytes) -> dict:
        """Parse raw data bytes into structured data.

        Args:
            decrypted: The decrypted bytes from the BLE advertisement.

        Returns:
            A dictionary containing the parsed data fields.

        """
