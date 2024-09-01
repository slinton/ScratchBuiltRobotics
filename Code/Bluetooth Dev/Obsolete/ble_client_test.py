#
# BLE Client Test
#
import uasyncio as asyncio
from ble_client import BLEClient
from machine import Pin

led = Pin(2, Pin.OUT)


def receive_message(message):
    print(f'Received message: {message}')
    if message == 'on':
        led.value(1)
    else:
        led.value(0)
        

client = BLEClient(
    name='BLE Test',
    receive_message_func=receive_message,
    receive_interval_ms=2000)

asyncio.run(client.start())