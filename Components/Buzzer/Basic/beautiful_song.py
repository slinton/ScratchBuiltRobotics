from machine import Pin, PWM
from time import sleep

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

dc = 32765 # 50%
q = 0.25   # delay for quarter note
h = 0.5

buzzer = PWM(Pin(13))
notes = [C, D, E, C, D, E, D, C, D, E, C, C]
delays = [q, q, h, q, q, h, q, q, q, q, h, h]

for i in range(len(notes)):
    buzzer.freq(notes[i])
    buzzer.duty_u16(dc)
    sleep(delays[i])
    buzzer.duty_u16(0)
    sleep(0.1)
    






