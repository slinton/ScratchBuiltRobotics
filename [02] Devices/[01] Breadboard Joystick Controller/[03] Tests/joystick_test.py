#
# JoystickTest
#
# Version: 1.00
# Date: 2025-05-30
# Sam Linton
#
# This script reads the values from a joystick connected to a Raspberry Pi Pico.
# It uses the ADC pins for the joystick axes and a GPIO pin for the button. 

from machine import Pin, ADC
from time import sleep

x = ADC(26)
y = ADC(27)
button = Pin(2, Pin.IN, Pin.PULL_UP)

while True:
    x_value = x.read_u16()
    y_value = y.read_u16()
    print(f'{x_value}, {y_value}, {button.value()}')
    sleep(0.1)