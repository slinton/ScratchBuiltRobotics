from machine import Pin, I2C
from time import sleep

from ads1x15 import ADS1115

SCL = 1
SDA = 0

i2c = I2C(0, scl=SCL, sda=SDA)
adc = ADS1115(i2c, address=72, gain=1)
print(i2c)

print(i2c.scan())
print(dir(i2c))
rate = 4

while True:
    ch0 = adc.read(rate, 0)
    ch1 = adc.read(rate, 1)
    ch2 = adc.read(rate, 2)
    ch3 = adc.read(rate, 3)
    print(f'{ch0}, {ch1}, {ch2}, {ch3}')
    sleep(0.05)
      

