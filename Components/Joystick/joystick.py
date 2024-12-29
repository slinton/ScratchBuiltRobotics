#
# JoystickController
#
from machine import Pin, I2C
from ads1x15 import ADS1115
from time import sleep

class JoystickController:
    def __init__(self, i2c, left, right, debug)-> None:
        print('init')
        self.left_button = Pin(left, Pin.IN, Pin.PULL_UP)
        self.right_button = Pin(right, Pin.IN, Pin.PULL_UP)
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
        message = f'{ch0}, {ch1}, {ch2}, {ch3}, {left_value}, {right_value}'
        return message


if __name__ == '__main__':
    i2c = I2C(1, scl=27, sda=26, freq=200_000)
    joystickController = JoystickController(i2c=i2c, left=18, right=28, debug=True)
    while True:
        message = joystickController.create_message()
        print(message)
        sleep(0.1)
