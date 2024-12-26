from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

width = 128
height = 32

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
print('I2C address : ' + hex(i2c.scan()[0]).upper())
print('I2C config  : ' + str(i2c))

oled = SSD1306_I2C(width, height, i2c)
# 
oled.fill(0)

oled.text('hi', 5, 8)
oled.show()