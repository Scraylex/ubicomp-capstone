import asyncio
import datetime
from multiprocessing import Manager
import os
from typing import Dict

from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError

from constants import ABS_PATH, OUTPUT_DIR


class VoiceListener:
    def __init__(self, shared_dict: Dict):
        self.RECOGNIZER = Recognizer()
        self.RECOGNIZER.dynamic_energy_threshold = False
        self.shared_dict = shared_dict

    async def listen(self):
        with Microphone() as source:
            print("Say something...")
            self.RECOGNIZER.adjust_for_ambient_noise(source)
            while not self.shared_dict['stop_record']:
                await asyncio.sleep(0.1)
                start_cmd = self.RECOGNIZER.listen(source)
                try:
                    start = self.RECOGNIZER.recognize_google_cloud(start_cmd, credentials_json=ABS_PATH)
                    print("Google Cloud Speech thinks you said " + start)
                    words = start.split()
                    if "start" in words[0]:
                        now = datetime.datetime.now()
                        unix_timestamp = int(now.timestamp())
                        filename = f"{words[1]}_{str(unix_timestamp)}"
                        print(f"Filename: {filename}")
                        directory = f"{OUTPUT_DIR}/{filename}/"
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        self.shared_dict['filename'] = directory
                        self.shared_dict['start_record'] = True
                    if "stop" in words:
                        print("Stop received")
                        self.shared_dict['stop_record'] = True
                        print("Exiting stop listener")
                except UnknownValueError as e:
                    print(f"Google Cloud Speech could not understand audio; {e}")
                except RequestError as e:
                    print(f"Could not request results from Google Cloud Speech service; {e}")
            print("shutting down recognizer")

    async def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())
        loop.close()

    @staticmethod
    async def main(shared_dict: Dict):
        voice = VoiceListener(shared_dict)
        await voice.start()


if __name__ == '__main__':
    with Manager() as manager:
        # Create a shared dictionary
        shared_dict = manager.dict({})
        # Create and start a process
        listener = VoiceListener(shared_dict)
        listener_task = asyncio.create_task(listener.listen())
        asyncio.gather(listener_task)
