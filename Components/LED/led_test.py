from machine import Pin
from time import sleep


if __name__ == '__main__':
    led = Pin(6, Pin.OUT)
    for _ in range(51):
        led.toggle()
        sleep(0.1)