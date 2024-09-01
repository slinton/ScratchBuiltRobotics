#
# BLE Server Test
#
# Version 24_07_31
#
import uasyncio as asyncio
from ble_server import BLEServer
from machine import Pin
from time import sleep
import random

button = Pin(0, Pin.IN, Pin.PULL_UP)

def button_pressed():
    message = 'off' if button.value() == 1 else 'on'
    print(f'Send message {message}')
    return message

def random_message():
    return str(random.randint(0, 9))


server = BLEServer(
    name='BLE Test',
    send_message_func=random_message,
    send_interval_ms=100)

asyncio.run(server.start())
