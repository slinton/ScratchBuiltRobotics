#
# scan_i2c
# V2025_04_05_01
#
from machine import Pin, I2C

# I2C pins for Raspberry Pi Pico (I2c id, SDA, SCL)
pin_sets = [ (0, 0, 1), (0, 4, 5), (0, 8, 9), (0, 12, 13), (0, 16, 17), (0, 20, 21),
             (1, 2, 3), (1, 6, 7), (1, 10, 11), (1, 14, 15), (1, 18, 19), (1, 26, 27)]

    
def test_all_i2cs():
    
    # Scan all I2C pin pairs 
    for pins in pin_sets:
        id, sda_pin, scl_pin = pins
        
        try:
            # Create the i2c object
            i2c = I2C(id=id, sda=Pin(sda_pin), scl=Pin(scl_pin))
            
            # Scan for the i2c
            devices = i2c.scan()
            
            # Print out devices I2C addresses found and the pins
            if len(devices) > 0:
                print(f'Found {len(devices)} devices on I2C {id}, sda = {sda_pin}, scl = {scl_pin}:')
                for device in devices:  
                    print(f'\tDecimal address: {device}  Hex address: {hex(device)}')
                print()
                
            # No devices found
            else:
                print(f'Found {len(devices)} devices on I2C {id}, sda = {sda_pin}, scl = {scl_pin}:')
                
        except:
            print(f'Incorrect I2C pins for I2c {id}: sda = {sda_pin}, scl = {scl_pin}')
        

test_all_i2cs()
