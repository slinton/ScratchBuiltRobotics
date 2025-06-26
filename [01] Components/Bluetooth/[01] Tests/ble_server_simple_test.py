#
# BLEServerSimpleTest
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
from ble_server import BLEServer

# Change this to the name of your BLE server
server_name = 'BLE Test'

def create_message():
    """This function creates a message to be sent over BLE."""
    return 'Hello, World!'


print(f'Starting BLE server {server_name}...')
server = BLEServer(
    name=server_name,
    create_message_func=create_message,
    send_interval_ms=100)

server.start()