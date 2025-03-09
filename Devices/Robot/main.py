#
# main
#
from robot import Robot
from claw import Claw
import uasyncio as asyncio

if __name__ == '__main__':
    robot = Robot(led_pin=6, buzzer_pin=22, claw=Claw())
    asyncio.run(robot.start())