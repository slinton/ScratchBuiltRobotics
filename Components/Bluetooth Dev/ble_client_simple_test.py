#
# BLE Client Simple Test
#
# Version 24_12_28_1
#
from ble_client import BLEClient


def receive_message(message):
    print(f'Received message: {message}')
    

client = BLEClient(
    server_name='BLE Test',
    receive_message_func=receive_message,
    receive_interval_ms=1000)
client.start()
print('Program terminated')
