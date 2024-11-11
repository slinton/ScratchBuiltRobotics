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
        led.on()
    else:
        led.off()
    

client = BLEClient(
    server_name='BLE Test',
    receive_message_func=receive_message,
    receive_interval_ms=1000)
client.start()
print('Program terminated')
#asyncio.run(client.start())