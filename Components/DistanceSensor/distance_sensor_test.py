#
# distance_sensor_test
#
# Version 2025_05_01_01
#
if __name__ == '__main__':
    distance_sensor = DistanceSensor(trig=20, echo=21)
    try:
        while True:
            print(distance_sensor.get_distance_cm())
            sleep(0.1)
            
    except KeyboardInterrupt:
        print('Program Ended')