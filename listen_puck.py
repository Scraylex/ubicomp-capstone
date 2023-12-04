from bleak import BleakScanner, BleakClient
import asyncio

def onDeviceChanged(addr, data):
    print(f"Device {addr}, value {data}")

devices = [
    "de:70:d9:0c:eb:86"
]

async def scan():
    scanner = BleakScanner()
    while True:
        devices_discovered = await scanner.discover()
        for device in devices_discovered:
            if device.address in devices:
                async with BleakClient(device) as client:
                    advertising_data = await client.read_gatt_char(0x16)  # Replace with the appropriate characteristic handle
                    data = bytes(advertising_data).decode("utf-8")
                    onDeviceChanged(device.address, data)

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
