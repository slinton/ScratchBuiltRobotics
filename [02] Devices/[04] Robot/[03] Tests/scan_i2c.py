#
# scan_i2c 
# Version 1.00
# Date: 2025-05-31
# Sam Linton
# This script scans all possible I2C pins on a Raspberry Pi Pico and prints the addresses of any connected devices.
#
from machine import Pin, I2C

# I2C pins for Raspberry Pi Pico (I2C id, SDA, SCL)
pin_sets = [ (0, 0, 1), (0, 4, 5), (0, 8, 9), (0, 12, 13), (0, 16, 17), (0, 20, 21),
             (1, 2, 3), (1, 6, 7), (1, 10, 11), (1, 14, 15), (1, 18, 19), (1, 26, 27)]

    
def test_all_i2cs():
    for pins in pin_sets:
        id, sda_pin, scl_pin = pins
        try:
            i2c = I2C(id=id, sda=Pin(sda_pin), scl=Pin(scl_pin))
            devices = i2c.scan()
            if len(devices) > 0:
                print(f'Found {len(devices)} devices on I2C {id}, sda = {sda_pin}, scl = {scl_pin}:')
                for device in devices:  
                    print(f'\tDecimal address: {device}  Hex address: {hex(device)}')
                print()
            else:
                print(f'Found {len(devices)} devices on I2C {id}, sda = {sda_pin}, scl = {scl_pin}:')
        except:
            print(f'Incorrect I2C pins for I2c {id}: sda = {sda_pin}, scl = {scl_pin}')
        

test_all_i2cs()