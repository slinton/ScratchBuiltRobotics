#
# double_joystick_test
#
# Version: 1.00
# Date: 2025-05-30
# Sam Linton
#
# This script reads the values from two joysticks connected to a Raspberry Pi Pico.
# It uses the ADC pins for the joystick axes and GPIO pins for the button. 
# Note that the second joystick's y-axis is not used in this example due to the limitations of the Pico's ADC pins.
from machine import Pin, ADC
from time import sleep

left_x = ADC(26)
left_y = ADC(27)
right_x = ADC(28)
l_button = Pin(2, Pin.IN, Pin.PULL_UP)
r_button = Pin(3, Pin.IN, Pin.PULL_UP)

while True:
    left_x_value = left_x.read_u16()
    left_y_value = left_y.read_u16()
    right_x_value = right_x.read_u16()
    right_y_value = 0
    
    message = f'{left_x_value},{left_y_value},{right_x_value},{right_y_value},{l_button.value()},{r_button.value()}'
    print(message)
    sleep(0.1)

