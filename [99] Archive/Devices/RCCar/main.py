#
# main
#
from rc_car import RCCar
from claw import Claw
import uasyncio as asyncio

if __name__ == '__main__':
    rc_car = RCCar(led_pin=6, buzzer_pin=22, claw=Claw())
    asyncio.run(rc_car.start())

