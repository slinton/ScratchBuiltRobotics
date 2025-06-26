#
# BLEClientSimpleTest
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A simple test script for a BLE client that receives and prints messages from a BLE server.
#
from ble_client import BLEClient

# Change this to the name of your BLE server
server_name = 'BLE Test'

def receive_message(message):
    print(f'Received message: {message}')
    

print(f'Starting BLE Client Simple Test, looking for server: {server_name}')
client = BLEClient(
    server_name=server_name,
    receive_message_func=receive_message,
    receive_interval_ms=1000)
client.start()