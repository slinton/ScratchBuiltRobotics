#
# BLE Server Simple Test
#
# Version 24_12_28
#
from ble_server import BLEServer

counter = 0

def create_message():
    global counter
    counter = (counter + 1) % 10
    return f'{counter}'


server = BLEServer(
    name='BLE Test',
    create_message_func=create_message,
    send_interval_ms=100)

server.start()