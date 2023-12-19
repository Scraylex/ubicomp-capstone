import asyncio
from multiprocessing import Manager
import threading

from constants import ADDRESSES
from nordic_ble_client import NordicBleClient
from video_manager import VideoManager
from voice_listener import VoiceListener


def run_in_new_loop(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coroutine)
    loop.close()


async def start():
    with Manager() as manager:
        shared_dict = manager.dict({})
        shared_dict['stop_record'] = False
        shared_dict['start_record'] = False
        shared_dict['record_ready'] = False
        shared_dict['ble_ready'] = False
        shared_dict['filename'] = None

        ble_client = NordicBleClient(ADDRESSES[0], shared_dict)
        video_manager = VideoManager(shared_dict)
        voice_listener = VoiceListener(shared_dict)

        ble_thread = threading.Thread(target=run_in_new_loop, args=(ble_client.start(),))
        video_thread = threading.Thread(target=run_in_new_loop, args=(video_manager.start(),))
        voice_thread = threading.Thread(target=run_in_new_loop, args=(voice_listener.listen(),))

        ble_thread.start()
        video_thread.start()
        voice_thread.start()

        ble_thread.join()
        video_thread.join()
        voice_thread.join()

if __name__ == '__main__':
    asyncio.run(start())
