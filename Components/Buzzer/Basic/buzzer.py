#
# buzzer.py
#
#
# Pins
# ----
# GP10 - buzzer +
# GND  - buzzer -
#
from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(10))
duty_cycle = 32000

while True:
    f = int(input('input frequency: '))
    buzzer.freq(f);
    buzzer.duty_u16(duty_cycle)
    sleep(1)
    buzzer.duty_u16(0)
