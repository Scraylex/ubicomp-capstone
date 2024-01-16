import asyncio
import time
from multiprocessing import Manager
from typing import Dict

import cv2


class VideoManager:
    def __init__(self, shared_dict: Dict):
        self.shared_dict = shared_dict

    async def start(self):
        capture = cv2.VideoCapture(0)
        print("Starting video capture")
        self.shared_dict['record_ready'] = True

        while not self.shared_dict['ble_ready']:
            print("Waiting for BLE to be ready")
            await asyncio.sleep(1)

        print("Recording")
        while not self.shared_dict['stop_record']:
            ret, frame = capture.read()
            if ret and self.shared_dict['start_record']:
                timestamp = int(time.time())
                cv2.imwrite(f'{self.shared_dict["filename"]}/{timestamp}.jpg', frame)
            await asyncio.sleep(1)
        capture.release()
        cv2.destroyAllWindows()
        self.shared_dict['record_ready'] = False
        print("Finished recording")


if __name__ == '__main__':
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict({})
        # Create and start a process
        video = VideoManager(shared_dict)

        video_task = asyncio.create_task(video.start())
        asyncio.gather(video_task)
