#
# beeautiful_song
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A simple script to play a beautiful song using a buzzer connected to a Raspberry Pi Pico.
#
# Pins
# ----
# GP22 - buzzer +
# GND  - buzzer -
#
from machine import Pin, PWM
from time import sleep

# Frequencies for musical notes
A  = 220
AS = 233
B  = 247
C  = 262
CS = 277
D  = 294
DS = 311
E  = 330
F  = 349
FS = 370
G  = 392
GS = 415

# Duty cycle for the buzzer (0-65535)
dc = 32765 # 50%
# Note durations in seconds
q = 0.25
h = 0.5

buzzer = PWM(Pin(22))
notes = [C, D, E, C, D, E, D, C, D, E, C, C]
delays = [q, q, h, q, q, h, q, q, q, q, h, h]

for i in range(len(notes)):
    buzzer.freq(notes[i])
    buzzer.duty_u16(dc)
    sleep(delays[i])
    buzzer.duty_u16(0)
    sleep(0.1)
    






