#
# Based on: https://github.com/robert-hh/QMC5883/tree/master
# NOTE: these devices are labeled as HMC5883L, which is a different device!

from machine import Pin, I2C
from qmc5883l import QMC5883L
from time import sleep

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
devices = i2c.scan()
print(f'Number of devices {len(devices)}')

mag = QMC5883L(i2c)
while True:
    (x, y, z, t) = mag.read_scaled()
    #print(f'{x}, {y}, {z}')
    print(f'{x}')
    sleep(0.1)
