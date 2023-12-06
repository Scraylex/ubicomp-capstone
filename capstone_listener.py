import asyncio
import csv
import datetime
import os
import time
from multiprocessing import Process, Pipe, Manager

import cv2
import winsound
from bleak import BleakScanner
from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError

OUTPUT_DIR = "../out"

RELATIVE_PATH = "./ubicomp-capstone-d784c94c5ff8.json"
ABS_PATH = os.path.abspath(RELATIVE_PATH)

CSV_HEADERS: list[str] = ["mac", "acc_x", "acc_y", "acc_z", "timestamp"]
DEVICES = [
    "E3:FE:49:99:DA:B2",
    "D7:D5:62:5C:F9:9D"
]

ACCEL_VALUES = []

RECOGNIZER = Recognizer()
RECOGNIZER.dynamic_energy_threshold = False

FILENAME = ""


# Function to emit a beep sound
def beep():
    winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 milliseconds


def record(start_event, stop_event) -> None:
    while not start_event.is_set():
        time.sleep(1)

    # Initialize the camera capture object
    capture = cv2.VideoCapture(0)  # Use 0 to capture video from the default camera
    # Define the codec and create a VideoWriter object
    codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video output (change as needed)
    output_file = f'{OUTPUT_DIR}/{FILENAME}.avi'  # Output video file name
    fps = 30  # Frames per second
    resolution = (640, 480)  # Resolution of the video (width, height)
    out = cv2.VideoWriter(output_file, codec, fps, resolution)
    # Check if the camera opened successfully
    if not capture.isOpened() or not out.isOpened():
        print("Error: Could not open camera or create video file.")

    print("Recording video")

    beep()
    while not stop_event.is_set():
        ret, frame = capture.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame")
            break

        # Write the frame to the video file
        out.write(frame)

    print("Stopping video")
    capture.release()
    out.release()
    cv2.destroyAllWindows()
    return


def listen(start_event, stop_event):
    with Microphone() as source:
        print("Say something...")
        RECOGNIZER.adjust_for_ambient_noise(source)
        while not stop_event.is_set():
            start_cmd = RECOGNIZER.listen(source)
            try:
                start = RECOGNIZER.recognize_google_cloud(start_cmd, credentials_json=ABS_PATH)
                print("Google Cloud Speech thinks you said " + start)
                words = start.split()
                if "start" in words[0]:
                    now = datetime.datetime.now()
                    unix_timestamp = int(now.timestamp())
                    if not start_event.is_set():
                        filename = f"{words[1]}_{str(unix_timestamp)}"
                        update_filename(filename)
                if "stop" in words:
                    print("Stop received")
                    stop_event.set()
                    print("Exiting stop listener")
            except UnknownValueError as e:
                print(f"Google Cloud Speech could not understand audio; {e}")
            except RequestError as e:
                print(f"Could not request results from Google Cloud Speech service; {e}")
        print("shutting down recognizer")
        return


def write_csv() -> None:
    with open(f'{OUTPUT_DIR}/{FILENAME}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)  # Write headers
        writer.writerows(ACCEL_VALUES)  # Write data rows


def scan(start_event, stop_event):
    while not start_event.is_set():
        time.sleep(1)
    scanner = BleakScanner()
    print("Starting BLE Advertisement scanner")
    while True:
        discover_task = asyncio.create_task(scanner.discover(return_adv=True))
        devices_discovered = asyncio.gather(discover_task)
        now = datetime.datetime.now()
        unix_timestamp = int(now.timestamp())
        for key, value in devices_discovered.items():
            if key in DEVICES:
                if value[1].manufacturer_data.values():
                    for elem in value[1].manufacturer_data.values():
                        result_list = [int(x) for x in str(elem.decode("utf-8")).split(',')]
                        ACCEL_VALUES.append([key, result_list[0], result_list[1], result_list[2], unix_timestamp])
        if stop_event.is_set():
            print("Shutting down BLE scanner")
            return


# Function for Process 2
def process_scanner(conn):
    print("Starting Scanner")
    received_data = conn.recv()
    print("Process 1 received:", received_data)
    conn.close()

# Function for Process 1
def process_video(conn):
    print("Starting Video")
    received_data = conn.recv()
    print("Process 1 received:", received_data)
    conn.close()

# Function for Process 1
def process_voice(conn):
    print("Starting Voice Recorder")
    received_data = conn.recv()
    print("Process 1 received:", received_data)
    conn.close()

def main():

    with Manager() as manager:
        now = datetime.datetime.now()
        unix_begin = int(now.timestamp())
        manager.dict({"filename": "", "begin": unix_begin, "end": 0})

        parent_record, child_video = Pipe()
        parent_conn_2, child_conn_2 = Pipe()
        parent_conn_2, child_conn_2 = Pipe()

        p1 = Process(target=process_one, args=(child_conn_1,))
        p2 = Process(target=process_two, args=(child_conn_2,))
        p2 = Process(target=process_two, args=(child_conn_2,))

        p1.start()
        p2.start()

    write_csv()


def update_filename(filename):
    global FILENAME
    FILENAME = filename


if __name__ == "__main__":
    main()
