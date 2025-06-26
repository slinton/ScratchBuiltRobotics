#
# oled_test 
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
# Pins
# ----
# GND  - OLED GND
# 3.3V - OLED +
# GP0  - OLED SDA
# GP1  - OLED SCL
#
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

width = 128
height = 32

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
print('I2C Address      : ' + hex(i2c.scan()[0]).upper())
print('I2C Configuration: ' + str(i2c))

oled = SSD1306_I2C(width, height, i2c)
oled.fill(0)
oled.line(0, 0, 127, 63, 1)
oled.text('Hello, world!', 5, 8)
oled.show()

# Other commands to try
# oled.fill(0)                         # fill entire screen with colour=0
# oled.pixel(0, 10)                    # get pixel at x=0, y=10
# oled.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
# oled.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
# oled.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
# oled.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
# oled.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
# oled.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
# oled.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
# oled.scroll(20, 0)                   # scroll 20 pixels to the right