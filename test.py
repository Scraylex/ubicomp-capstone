import asyncio
import csv
import datetime

from bleak import BleakScanner

FILENAME = "asd"
ACCEL_VALUES = []
OUTPUT_DIR = "../out"
CSV_HEADERS: list[str] = ["mac", "acc_x", "acc_y", "acc_z", "timestamp"]
DEVICES = [
    "E3:FE:49:99:DA:B2",
    "D7:D5:62:5C:F9:9D"
]

COUNTER = 100000
def write_csv() -> None:
    with open(f'{OUTPUT_DIR}/{FILENAME}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)  # Write headers
        writer.writerows(ACCEL_VALUES)  # Write data rows


async def scan():
    scanner = BleakScanner()
    print("Starting BLE Advertisement scanner")
    cnt = 0
    while cnt < COUNTER:
        discover_task = await scanner.discover(return_adv=True)
        devices_discovered = discover_task
        now = datetime.datetime.now()
        unix_timestamp = int(now.timestamp())
        for key, value in devices_discovered.items():
            if key in DEVICES:
                if value[1].manufacturer_data.values():
                    for elem in value[1].manufacturer_data.values():
                        result_list = [int(x) for x in str(elem.decode("utf-8")).split(',')]
                        ACCEL_VALUES.append([key, result_list[0], result_list[1], result_list[2], unix_timestamp])
                        cnt += 1
                        print(result_list)
    write_csv()


if __name__ == '__main__':
    asyncio.run(scan())
