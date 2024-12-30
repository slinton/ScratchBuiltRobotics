#
#
#
from machine import Pin
from servo import Servo
from utime import sleep

s = Servo(pin_id=28)
led = Pin(25, Pin.OUT)

while True:
    led.value(1)
    sleep(0.1)
    s.write(30)
    led.value(0)
    sleep(1)
    led.value(1)
    s.write(90)
    led.value(0)
    sleep(1)
