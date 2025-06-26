#
# DistanceSensor
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A class to measure distance using an ultrasonic sensor.
#
from machine import Pin
from time import sleep, sleep_us, ticks_us

class DistanceSensor:
    """Class to get distance to features in front """
    
    def __init__(self, trig=20, echo=21)-> None:
        """Constructor

        Args:
            trig (int): pin number for trig
            echo (int): pin number for echo
        """
        
        self._trig_pin = Pin(trig, Pin.OUT)
        self._echo_pin = Pin(echo, Pin.IN)
        
    def get_distance_cm(self)-> float:
        """Get distance in cm

        Returns:
            float: distance in cm
        """

        # trig the ultrasonic pulse
        self._trig_pin.value(0)
        sleep_us(2)
        self._trig_pin.value(1)
        sleep_us(10)
        self._trig_pin.value(0)
        
        # Start timing the signal from the echo pin
        count = 0
        while self._echo_pin.value() == 0 and count < 100_000:
            count += 1
        t1 = ticks_us()
        
        # Finish timing the signal from the echo pin
        count = 0
        while self._echo_pin.value() == 1 and count < 100_000:
            count += 1
        t2 = ticks_us()
        
        # Echo pin signal duration indicates time of flight
        return (t2 - t1) * 0.034 / 2
    
    
if __name__ == '__main__':
    distance_sensor = DistanceSensor(trig=20, echo=21)
    try:
        while True:
            print(distance_sensor.get_distance_cm())
            sleep(0.1)
            
    except KeyboardInterrupt:
        print('Program Ended')
