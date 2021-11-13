from contextlib import contextmanager
from typing import Optional

import hid
from loguru import logger


class CO2monitor:
    """ID 04D9:A052 Holtek Semiconductor."""

    def __init__(self) -> None:
        self.device = hid.device()

    def hid_open(self) -> None:
        self.device.open(0x04d9, 0xa052)
        logger.debug('Opened')
        self.device.send_feature_report((0, 0, 0, 0, 0, 0, 0, 0))

    @contextmanager
    def co2hid(self):
        self.hid_open()
        try:
            yield
        finally:
            self.device.close()
            logger.debug('Closed')

    def decode_message(
        self,
        msg: list[int],
    ) -> tuple[Optional[int], Optional[float]]:
        hex_msg = [
            f'0x{item:X}' if item >= 0x10 else f'0x0{item:X}'
            for item in msg
        ]
        logger.debug(f'Got a message: {hex_msg}')

        bad_msg = (msg[5] != 0) or (msg[6] != 0) or (msg[7] != 0)
        bad_msg |= msg[4] != 0x0D
        bad_msg |= (sum(msg[:3]) & 0xFF) != msg[3]
        if bad_msg:
            return None, None

        value = (msg[1] << 8) | msg[2]

        if msg[0] == 0x50:
            return int(value), None
        elif msg[0] == 0x42:
            return None, value / 16 - 273.15
        else:
            return None, None

    def read_device(
        self,
        max_attempts: int = 50,
    ) -> tuple[Optional[int], Optional[float]]:
        co2 = None
        temp = None
        for _ in range(max_attempts):
            try:
                draft_co2, draft_temp = self.decode_message(
                    self.device.read(8),
                )
            except ValueError:
                logger.error('Error on device reading')
                return co2, temp
            if draft_co2 is not None:
                co2 = draft_co2
            if draft_temp is not None:
                temp = draft_temp
            if co2 is not None and temp is not None:
                break
        return co2, temp

    def read_data(
        self,
        max_attempts: int = 50,
    ) -> tuple[Optional[int], Optional[float]]:
        try:
            with self.co2hid():
                return self.read_device(max_attempts=max_attempts)
        except OSError:
            logger.error('Error on device opening ')
            return None, None
