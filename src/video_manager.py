import asyncio
import time
from multiprocessing import Manager
from typing import Dict
from constants import ADDRESSES, DURATION
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

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = capture.get(cv2.CAP_PROP_FPS)
        print(fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        timestamp = int(time.time())
        output = cv2.VideoWriter(f'../test_data/{timestamp}.mp4', fourcc, fps, (width, height))

        print("Recording")
        self.shared_dict['start_record'] = True
        start_time = time.time()
        while True:
            ret, frame = capture.read()
            #cv2.imshow('Capture', frame) does not work in multithreading
            output.write(frame)
            elapsed_time = time.time() - start_time
            if elapsed_time >= DURATION:
                self.shared_dict['stop_record'] = True
                break
        capture.release()
        cv2.destroyAllWindows()
        self.shared_dict['record_ready'] = False
        print("Finished recording")


if __name__ == '__main__':
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict({})
        shared_dict['stop_record'] = False
        shared_dict['start_record'] = True
        shared_dict['record_ready'] = False
        shared_dict['ble_ready'] = False
        shared_dict['filename'] = None
        # Create and start a process
        video = VideoManager(shared_dict)

        asyncio.run(video.start())

        #video_task = asyncio.create_task(video.start())
        #asyncio.gather(video_task)
