#
# BLE JoystickController Client Test
#
# Version 24_07_31_00
#
import uasyncio as asyncio
from ble_client import BLEClient
from machine import Pin

led = Pin(2, Pin.OUT)

def receive_message(message):
#     print(f'{message}')
    hex_values = message.split(',')
    values = [int(hex_value, 16) for hex_value in hex_values]
    print (values)
    

    
if __name__ == '__main__':
    try:    
        client = BLEClient(
            server_name='BLE Test',
            receive_message_func=receive_message,
            receive_interval_ms=1000)
        client.start()
        #asyncio.run(client.start())
        
    except KeyboardInterrupt:
        print('Program terminated')





