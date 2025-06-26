#
# Test
#
from machine import Pin, SPI
from time import sleep
from ili9341 import Display, color565


led = Pin('LED', Pin.OUT)

spi = SPI(0, baudrate=40_000_000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
display.clear()

sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
display.draw_sprite(sprite, 50, 70, 41, 49)

display.draw_line(30, 30, 120, 140, color565(0, 255, 0))

for _ in range(10):
    led.toggle()
    sleep(0.1)