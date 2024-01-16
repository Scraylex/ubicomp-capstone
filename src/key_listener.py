import asyncio
import datetime
import os
from multiprocessing import Manager
from typing import Dict

import keyboard

from constants import OUTPUT_DIR


class KeyListener:
    def __init__(self, shared_dict: Dict):
        self.shared_dict = shared_dict

    async def listen(self):
        print("Press 'r' to start recording...")
        while not self.shared_dict['stop_record']:
            await asyncio.sleep(0.1)
            if keyboard.is_pressed('r'):
                filename = input("Enter filename: ")
                now = datetime.datetime.now()
                unix_timestamp = int(now.timestamp())
                filename = f"{filename}_{str(unix_timestamp)}"
                print(f"Filename: {filename}")
                directory = f"{OUTPUT_DIR}/{filename}/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                self.shared_dict['filename'] = directory
                self.shared_dict['start_record'] = True
                print("Recording started. Press 'r' again to stop recording...")
                while self.shared_dict['start_record']:
                    await asyncio.sleep(0.1)
                    if keyboard.is_pressed('r'):
                        print("Stop received")
                        self.shared_dict['stop_record'] = True
                        print("Exiting stop listener")
                        break

    async def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())
        loop.close()

    @staticmethod
    async def main(shared_dict: Dict):
        voice = KeyListener(shared_dict)
        await voice.start()


if __name__ == '__main__':
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict({})
        # Create and start a process
        listener = KeyListener(shared_dict)
        listener_task = asyncio.create_task(listener.listen())
        asyncio.gather(listener_task)
