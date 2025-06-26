#
# BLEServerSimpleTest
#
# Version 1.00
# Date: 2025-0-30
# Sam Linton
#
from ble_server import BLEServer

counter = 0

def create_message():
    return 'Hello, World!'


print('Starting BLE server...')
server = BLEServer(
    name='BLE Test',
    create_message_func=create_message,
    send_interval_ms=100)

server.start()