import asyncio
import os
import struct
from multiprocessing import Manager
from typing import Dict
import time
from bleak import BleakClient, discover, BleakScanner

import csv_writer
from constants import GYRO_CHAR_HAND, GYRO_CHAR_LEG, ADDRESSES, DURATION


class NordicBleClient:
    def __init__(self, address, shared_dict: Dict):
        self.address_hand = address[0]
        self.address_leg = address[1]
        self.data_received = False
        self.data_array = []
        self.client_1 = None
        self.client_2 = None
        self.shared_dict = shared_dict

    async def start(self) -> None:
        try:
            # Get UUIDs of the puckJS devices (optional debug step)
            devices = await BleakScanner.discover()
            for d in devices:
                print(d)

            print("Connecting to BLE devices")
            self.client_1 = BleakClient(self.address_hand)
            self.client_2 = BleakClient(self.address_leg)

            # Connect both clients in parallel
            await asyncio.gather(
                self.client_1.connect(),
                self.client_2.connect()
            )
            print("Both devices connected")

            self.shared_dict['ble_ready'] = True

            # Wait until record_ready is True
            while not self.shared_dict['record_ready']:
                await asyncio.sleep(1)

            # Start notifications in parallel
            await asyncio.gather(
                self.client_1.start_notify(GYRO_CHAR_HAND, self._uart_data_received),
                self.client_2.start_notify(GYRO_CHAR_LEG, self._uart_data_received)
            )
            print("Started notifications on both devices")

            # Wait for duration, then monitor for stop
            await asyncio.sleep(DURATION)
            while not self.shared_dict['stop_record']:
                if not self.data_received:
                    break
                self.data_received = False

            print(f"Done for {self.address_hand}")
            print(f"Done for {self.address_leg}")

        except Exception as e:
            print(e)
            raise e
        finally:
            await self.stop()

    async def stop(self) -> None:
        if self.client_1:
            await self.client_1.stop_notify(GYRO_CHAR_HAND)
            await self.client_1.disconnect()
            print("Disconnected hand device")

        if self.client_2:
            await self.client_2.stop_notify(GYRO_CHAR_LEG)
            await self.client_2.disconnect()
            print("Disconnected leg device")

        print("Writing to csv")
        new_path = f'../test_data/test_{int(time.time())}'
        os.makedirs(new_path, exist_ok=True)
        csv_writer.write_csv(self.data_array, new_path)
        print("Done writing to csv")

    def _uart_data_received(self, sender, data: bytearray) -> None:
        self.data_received = True
        if self.shared_dict['start_record']:
            values = struct.unpack('<iiiiiif', data) # f-- to interpret temperature in float
            values = [val for val in values]

            # Determine source
            label = None
            if sender.uuid == GYRO_CHAR_HAND.lower():
                label = "hand"
            elif sender.uuid == GYRO_CHAR_LEG.lower():
                label = "leg"

            values.append(time.time())
            values.append(label)
            print(values)
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

        client = NordicBleClient(ADDRESSES, shared_dict)

        asyncio.run(client.start())
