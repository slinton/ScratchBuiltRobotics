#
# BLE Server
#
import sys

import aioble
import bluetooth
from machine import Pin
import uasyncio as asyncio
from micropython import const

def uid():
    '''
    Return the unique id of the defice as a string
    '''
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *machine.unique_id())

MANUFACTURER_ID = const(0x02A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0x2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)

_ENV_SENSE_UUID = bluetooth.UUID(0x180A)
_GENERIC = bluetooth.UUID(0x1848)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x1800)
_BUTTON_UUID = bluetooth.UUID(0x2A6E)

_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

# Advertising frequency
ADV_INTERVAL_MS = 250_000

device_info = aioble.Service(_ENV_SENSE_UUID)

connection = None

# Create characteristics for device info
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="KevsRobotsRemote")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="1.0")

remote_service = aioble.Service(_GENERIC)

button_characteristic = aioble.Characteristic(
    remote_service,
    _BUTTON_UUID,
    read = True,
    notify = False
)

print('registering services')

connected = False

# Wait for connection; Don't advertise whie connected
async def peripheral_task():
    print('peripheral task')
    global connected, connection
    while True:
        connected = False
        async with await aioble.advertise(
            ADV_INTERVAL_MS, 
            name="server", 
            appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
            services=[_ENV_SENSE_TEMP_UUID]
        ) as connection:
            print("Connection from", connection.device)
            connected = True
            print(f"connected: {connected}")
            await connection.disconnected()
            print(f'disconnected')
            
async def remote_task():
    '''
    Send the command
    '''
    while True:
        if connected:
            print('sent')
            button_characteristic.write(b'a')
            button_characteristic.notify(connection, b'a')
            await asyncio.sleep_ms(1000)
        else:
            print('not connected')
            await asyncio.sleep_ms(1000)
    

async def main():
    tasks = [
        asyncio.create_task(peripheral_task()),
        asyncio.create_task(remote_task())
    ]
    await asyncio.gather(*tasks)
    
asyncio.run(main())



