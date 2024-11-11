#
<<<<<<< HEAD
# BLE Joystick Controller Client Test
=======
# BLE Client Test
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
#
import uasyncio as asyncio
from ble_client import BLEClient
from machine import Pin

led = Pin(2, Pin.OUT)


def receive_message(message):
<<<<<<< HEAD
    print(f'{message}')
=======
    print(f'Received message: {message}')
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
    if message == 'on':
        led.on()
    else:
        led.off()
    

client = BLEClient(
    server_name='JoystickController',
    receive_message_func=receive_message,
    receive_interval_ms=1000)
client.start()
print('Program terminated')
<<<<<<< HEAD
#asyncio.run(client.start())
=======
#asyncio.run(client.start())
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
