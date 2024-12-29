#
# BLEJoystickController
#
# Version 24_12_28_1
#
from machine import Pin, I2C
from ads1x15 import ADS1115
from ble_server import BLEServer
from time import sleep

class BLEJoystickController(BLEServer):
    def __init__(self, i2c, left: int, right: int, name:str="JoystickController", led: int=None, debug: bool=False)-> None:
        BLEServer.__init__(self, 
                           name=name,
                           create_message_func = self.create_message,
                           on_connected_func=self.on_connected,
                           on_disconnected_func=self.on_disconnected,
                           send_interval_ms=100)
        self.left_button = Pin(left, Pin.IN, Pin.PULL_UP)
        self.right_button = Pin(right, Pin.IN, Pin.PULL_UP)
        self.led = None if led == None else Pin(led, Pin.OUT)
        self.adc = ADS1115(i2c, address=72, gain=1)
        self.rate = 4
        self.debug = debug
        
    def create_message(self)-> str:
        ch0 = hex(max(0, self.adc.read(self.rate, 0)))[2:]
        ch1 = hex(max(0, self.adc.read(self.rate, 1)))[2:]
        ch2 = hex(max(0, self.adc.read(self.rate, 2)))[2:]
        ch3 = hex(max(0, self.adc.read(self.rate, 3)))[2:]
        left_value = 1 - self.left_button.value()
        right_value = 1 - self.right_button.value()
        button_code = left_value + 2 * right_value
        message = f'{ch0},{ch1},{ch2},{ch3},{button_code}'
        return message
            
    def on_connected(self):
        print('Connected')
        if self.led != None:
            self.led.value(1)
            
    def on_disconnected(self):
        print('Disconnected!')
        if self.led != None:
            self.led.value(0)


if __name__ == '__main__':
    try:
        i2c = I2C(0, scl=1, sda=0, freq=200_000)
        joystickController = BLEJoystickController(name="JoystickController", i2c=i2c, left=2, right=3, led=6, debug=True)
        joystickController.start()
    
    except KeyboardInterrupt:
        print('Program terminated')
    
