import os

GYRO_SERVICE_HAND = '0000bcde-0000-1000-8000-00805f9b34fb'
GYRO_CHAR_HAND = '0000abcd-0000-1000-8000-00805f9b34fb'
GYRO_SERVICE_LEG = '0000180D-0000-1000-8000-00805F9B34FB'
GYRO_CHAR_LEG = '0000180A-0000-1000-8000-00805F9B34FB'
DATA_KEYS = ["accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "temp", "timestamp", "sender"]
OUTPUT_DIR = "../collected"
RELATIVE_PATH = "../ubicomp-capstone-d784c94c5ff8.json"
ABS_PATH = os.path.abspath(RELATIVE_PATH)
ADDRESSES = [
    "A33FA688-A0DE-0557-466C-6844BC3314B5",
    "07A37B5B-15D1-A869-3F47-16A832C90BF9"
]
# after adding and 1st trial to connect to new address, restarting (mac) machines helps solve gyro_char not found
# error: bleak.exc.BleakCharacteristicNotFoundError: Characteristic 0000abcd-0000-1000-8000-00805f9b34fb was not found!
DURATION = 120
