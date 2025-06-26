# servo.py
# Kevin McAleer
# March 2021
# Added in test method - SL

from pca9685 import PCA9685
import math


class Servos:
    def __init__(self, i2c, address=0x40, freq=50, min_us=600, max_us=2400,
                 degrees=180):
        self.period = 1000000 / freq
        self.min_duty = self._us2duty(min_us)
        self.max_duty = self._us2duty(max_us)
        self.degrees = degrees
        self.freq = freq
        self.pca9685 = PCA9685(i2c, address)
        self.pca9685.freq(freq)

    def _us2duty(self, value):
        return int(4095 * value / self.period)

    def position(self, index, degrees=None, radians=None, us=None, duty=None):
        span = self.max_duty - self.min_duty
        if degrees is not None:
            duty = self.min_duty + span * degrees / self.degrees
        elif radians is not None:
            duty = self.min_duty + span * radians / math.radians(self.degrees)
        elif us is not None:
            duty = self._us2duty(us)
        elif duty is not None:
            pass
        else:
            return self.pca9685.duty(index)
        duty = min(self.max_duty, max(self.min_duty, int(duty)))
        print(f'position {degrees=} {duty=}')
        self.pca9685.duty(index, duty)

    def release(self, index):
        self.pca9685.duty(index, 0)
        
        
        
        
if __name__ == "__main__":
    # Test code
    from machine import I2C
    from time import sleep

    # Create I2C object
    i2c = I2C(0, sda=0, scl=1)
    print(f'Found {len(i2c.scan())} i2c devices.')
    
    # Create servo info objects
    servos = Servos(i2c)
    
    i2c.writeto_mem(0x40, 0x06,  b'\x00\x00\x8e\x00')
    sleep(0.5)
    i2c.writeto_mem(0x40, 0x06, b'\x00\x00\xd6\x01')
    sleep(0.5)
    i2c.writeto_mem(0x40, 0x06,  b'\x00\x00\x8e\x00')
    
    
#     
#     servos.position(0, degrees=10)
#     sleep(0.5)
#     servos.position(0, degrees=170)
#     sleep(0.5)

