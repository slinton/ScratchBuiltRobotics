#
# distance_sensor_test
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A simple test script for the DistanceSensor class to measure distance using an ultrasonic sensor.
#
if __name__ == '__main__':
    distance_sensor = DistanceSensor(trig=20, echo=21)
    try:
        while True:
            print(distance_sensor.get_distance_cm())
            sleep(0.1)
            
    except KeyboardInterrupt:
        print('Program Ended')