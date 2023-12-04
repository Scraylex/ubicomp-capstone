import asyncio
import datetime
import os
import threading

import cv2
import winsound
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

relative_path = "./ubicomp-capstone-d784c94c5ff8.json"
absolute_path = os.path.abspath(relative_path)


# Function to emit a beep sound
def beep():
    winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 milliseconds


recognizer = Recognizer()


async def capture_video(filename: str, event: asyncio.Event) -> None:
    # Initialize the camera capture object
    capture = cv2.VideoCapture(0)  # Use 0 to capture video from the default camera
    # Define the codec and create a VideoWriter object
    codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video output (change as needed)
    output_file = f'{filename}.avi'  # Output video file name
    fps = 30  # Frames per second
    resolution = (640, 480)  # Resolution of the video (width, height)
    out = cv2.VideoWriter(output_file, codec, fps, resolution)
    # Check if the camera opened successfully
    if not capture.isOpened() or not out.isOpened():
        print("Error: Could not open camera or create video file.")

    print("Recording video")

    thread = threading.Thread(target=stop_task_listener, args=(event,))
    thread.start()

    beep()
    while not event.is_set():
        ret, frame = capture.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame")
            break

        # Write the frame to the video file
        out.write(frame)

    thread.join()

    print("Stopping video")
    capture.release()
    out.release()
    cv2.destroyAllWindows()


def stop_task_listener(event):
    with Microphone() as source:
        print("Listening for stop")
        stop_cmd = recognizer.listen(source, timeout=6000)
        stop = recognizer.recognize_google_cloud(stop_cmd, credentials_json=absolute_path)
        if "stop" in stop:
            print("Stop received")
            event.set()
        print("Exiting stop listener")


async def listen():
    with Microphone() as source:
        print("Say something...")
        start_cmd = recognizer.listen(source)
        try:
            start = recognizer.recognize_google_cloud(start_cmd, credentials_json=absolute_path)
            print("Google Cloud Speech thinks you said " + start)
            words = start.split()
            if "start" in words[0]:
                now = datetime.datetime.now()
                unix_timestamp = int(now.timestamp())
                # Emit a beep in response
                filename = f"{words[1]}_{str(unix_timestamp)}"
                # Start the subprocess
                event = asyncio.Event()

                capture_video_task = asyncio.create_task(capture_video(filename, event))

                await asyncio.gather(capture_video_task)

                print("Exiting Listener")
            else:
                print("exiting programm. Did not receive start command")
        except UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except RequestError as e:
            print(f"Could not request results from Google Cloud Speech service; {e}")
        finally:
            print("shutting down recognizer")


if __name__ == "__main__":
    asyncio.run(listen())
