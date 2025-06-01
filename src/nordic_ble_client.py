import asyncio
import struct
from multiprocessing import Manager
from typing import Dict

import time
from bleak import BleakClient, discover, BleakScanner

import csv_writer
from constants import GYRO_CHAR, ADDRESSES, DURATION


class NordicBleClient:
    def __init__(self, address, shared_dict: Dict):
        self.address = address
        self.data_received = False
        self.data_array = []
        self.client = None
        self.shared_dict = shared_dict

    async def start(self) -> None:
        try:
            # get UUID of the puckJS to update the address for MacOS
            devices = await BleakScanner.discover()
            for d in devices:
                print(d)
            print("Connecting to BLE device")
            self.client = BleakClient(self.address)
            await self.client.connect()
            print("Connected to device")
            self.shared_dict['ble_ready'] = True
            while not self.shared_dict['record_ready']:
                await asyncio.sleep(1)
            await self.client.start_notify(GYRO_CHAR, self._uart_data_received)
            await asyncio.sleep(DURATION)
            while not self.shared_dict['stop_record']:
                if not self.data_received:
                    break
                self.data_received = False
            print(f"Done for {self.address}")
        except Exception as e:
            print(e)
            raise e
        finally:
            await self.stop()

    async def stop(self) -> None:
        await self.client.stop_notify(GYRO_CHAR)
        await self.client.disconnect()
        print("Disconnected")
        print("Writing to csv")
        csv_writer.write_csv(self.data_array, '../data')
        print("Done writing to csv")

    def _uart_data_received(self, sender, data: bytearray) -> None:
        self.data_received = True
        if self.shared_dict['start_record']:
            values = struct.unpack('<iiiiiii', data)
            values = [val for val in values]
            print(values)
            values.append(time.time())
            values.append(sender.description)
            self.data_array.append(values)


if __name__ == '__main__':
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict({})
        shared_dict['stop_record'] = False
        shared_dict['start_record'] = True
        shared_dict['record_ready'] = True
        shared_dict['ble_ready'] = False
        shared_dict['filename'] = None

        client = NordicBleClient(ADDRESSES[0], shared_dict)

        asyncio.run(client.start())
