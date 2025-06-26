#
# buzzer_test
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A simple test script for a buzzer connected to a Raspberry Pi Pico.
#
# Pins
# ----
# GP22 - buzzer +
# GND  - buzzer -
#
from machine import Pin, PWM
from time import sleep


buzzer = PWM(Pin(22))
duty_cycle = 32000

while True:
    f = int(input('input frequency: '))
    buzzer.freq(f)
    buzzer.duty_u16(duty_cycle)
    sleep(1)
    buzzer.duty_u16(0)
