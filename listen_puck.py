from bleak import BleakScanner, BleakClient
import asyncio


def onDeviceChanged(addr, data):
    print(f"Device {addr}, value {data}")


devices = [
    "de:70:d9:0c:eb:86"
    "D7:D5:62:5C:F9:9D"
]


async def scan():
    scanner = BleakScanner()
    while True:
        devices_discovered = await scanner.discover()
        for device in devices_discovered:
            if device.address in devices:
                async with BleakClient(device) as client:



loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
