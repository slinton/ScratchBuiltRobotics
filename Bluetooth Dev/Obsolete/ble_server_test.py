#
# BLE Server Test
#
import uasyncio as asyncio
from ble_server import BLEServer
from machine import Pin

button = Pin(0, Pin.IN, Pin.PULL_UP)

def button_pressed():
    return 'on' if button.value() == 1 else 'off'

# count = 0
# def send_message_func():
#     global count
#     print(f'Update func, count = {count}')
#     count += 1
#     return str(count)

server = BLEServer(
    name='BLE Test',
    send_message_func=button_pressed,
    update_interval_ms=2000)

asyncio.run(server.start())