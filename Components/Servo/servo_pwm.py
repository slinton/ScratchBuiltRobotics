#
# servo.py
#
# Pins
# ----
# 3.3V - Servo +
# GP0  - Servo Signal
# GnD  - Servo GND
#
# 2% for zero degrees
# 12.5 % for 180
#
# Angle  Percent  Value
# -----  -------  -----
#   0     2.0%     1350
# 180    12.5%     8200

from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(0))
pwm.freq(50)


def degrees_to_value(degrees):
    return 1350 + int(38.06 * degrees) 
    
while True:
    pwm.duty_u16(degrees_to_value(10))
    sleep(2)
    pwm.duty_u16(degrees_to_value(170))
    sleep(2)


