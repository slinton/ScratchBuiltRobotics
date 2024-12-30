from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

width = 128
height = 32

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)
print('I2C Address      : ' + hex(i2c.scan()[0]).upper())
print('I2C Configuration: ' + str(i2c))

oled = SSD1306_I2C(width, height, i2c)
x = 0
y = 0
u = 1
v = 1

while True:
    oled.fill(0)
    oled.rect(x, y, 5, 2, 1)
    oled.show()
    x += u
    y += v
    if x < 0 or x > width:
        u = -u
    if y < 0 or y > height:
        v = -v
