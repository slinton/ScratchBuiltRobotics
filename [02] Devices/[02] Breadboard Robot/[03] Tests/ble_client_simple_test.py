#
# BLEClientSimpleTest
#
# Version 1.00
# Date: 2025-05-30
# Sam Linton
#
from ble_client import BLEClient


def receive_message(message):
    print(f'Received message: {message}')
    

print('Starting BLE Client Simple Test')
client = BLEClient(
    server_name='BLE Test',
    receive_message_func=receive_message,
    receive_interval_ms=1000)
client.start()