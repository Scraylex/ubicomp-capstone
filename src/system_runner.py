import asyncio
from multiprocessing import Manager
import threading

import cv2

from constants import ADDRESSES
#from nordic_ble_client import NordicBleClient
from nordic_ble_multiclient import NordicBleClient
from video_manager import VideoManager

# from key_listener import KeyListener


def run_in_new_loop(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coroutine)
    loop.close()


def run_cam(cam_routine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cam_routine)
    loop.close()


async def start():
    with Manager() as manager:
        shared_dict = manager.dict({})
        shared_dict['stop_record'] = False
        shared_dict['start_record'] = False
        shared_dict['record_ready'] = False
        shared_dict['ble_ready'] = False
        shared_dict['filename'] = None

        ble_client = NordicBleClient(ADDRESSES, shared_dict)
        video_manager = VideoManager(shared_dict)
        # voice_listener = KeyListener(shared_dict)

        ble_thread = threading.Thread(target=run_in_new_loop, args=(ble_client.start(),))
        video_thread = threading.Thread(target=run_cam, args=(video_manager.start(), ), daemon=True)
        # voice_thread = threading.Thread(target=run_in_new_loop, args=(voice_listener.listen(),))

        ble_thread.start()
        video_thread.start()
        # voice_thread.start()

        ble_thread.join()
        video_thread.join()
        # voice_thread.join()


if __name__ == '__main__':
    asyncio.run(start())
