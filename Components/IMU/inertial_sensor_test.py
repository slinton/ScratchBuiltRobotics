#
# mpu6050.py
#
# Pins
# ----
# 3V3 - VCC
# GND - GND
# GP0 - SDA
# GP1 = SCL
#
from inertial_sensor import InertialSensor
from time import sleep
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = InertialSensor(i2c, heading_threshold=0.3)
imu.calibrate()

while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    temp=round(imu.temperature,2)
    #print(f'{ax},{ay},{az}')
    #print(f'{{gx},{gy},{gz')
    #print(f'{temp}')
    imu.update()
    print(f'{imu.raw_heading}')
    sleep(0.01)
