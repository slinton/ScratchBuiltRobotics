#
# BLEServerTest
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A simple test script for a BLE server that sends messages at regular intervals.
from ble_server import BLEServer

# Change this to the name of your BLE server
server_name = 'BLE Test'
counter = 0

def create_message():
    """Create a message to be sent over BLE."""
    global counter
    counter = (counter + 1) % 10
    return f'{counter}'


if __name__ == '__main__':
    try:
        print('Starting BLE server...')
        server = BLEServer(
            name=server_name,
            create_message_func=create_message,
            send_interval_ms=100)

        server.start()

    except KeyboardInterrupt:
        print('Stopping BLE server...')
        server.stop()

    except Exception as e:
        print(f'Error: {e}')
        server.stop()