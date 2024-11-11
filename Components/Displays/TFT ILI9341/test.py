from machine import Pin, SPI
# from random import random, seed
from ili9341 import Display, color565
# from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff
# from xglcd_font import XglcdFont


spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
display.clear()

# Load sprite
sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
display.draw_sprite(sprite, 50, 70, 41, 49)