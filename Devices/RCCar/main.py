#
# main
#
from rc_car import RCCar
import uasyncio as asyncio

if __name__ == '__main__':
    rc_car = RCCar(led_pin=9, buzzer_pin=22)
    asyncio.run(rc_car.start())