#
# BLEClientTest
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
from ble_client import BLEClient


def receive_message(message):
    print(f'Received message: {message}')
    

if __name__ == '__main__':
    try:
        print('Starting BLE Client Test')
        client = BLEClient(
        server_name='BLE Test',
        receive_message_func=receive_message,
        receive_interval_ms=1000)
        client.start()

    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting...')
        exit(0)

    except Exception as e:
        print(f'An error occurred: {e}')
        exit(1)