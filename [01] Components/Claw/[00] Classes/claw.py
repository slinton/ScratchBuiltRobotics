#
# Claw
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A  claw control class that uses a gripper and lifter.
#
# TODO: Refactor to remove hardcoded values and improve readability.
#
import uasyncio as asyncio
from gripper import Gripper
from lifter import Lifter
from time import sleep

class Claw:
    gain: float = 30.0
    
    def __init__(self, gripper_pin: int = 17, lifter_pin: int = 16)-> None:
        # self.running = False
        self.gripper = Gripper(pin=gripper_pin)
        self.lifter = Lifter(pin=lifter_pin)
        
        sleep(0.5)
        self.gripper.close()
        self.lifter.lift()
        sleep(0.5)
       
    def receive_message(self, message)-> str:
        """Receive a message from (e.g.) joystick and process it.
        Args:
            message (str): The message received from the BLE client.
        Returns:
            str: A response message.
        """
        #print(f'Message: {message}')
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
        print(vals)
        
        # TODO: clean up this ugliness
        if vals[1] - 13447 > 400:
            self.gripper.start_open()
        elif vals[1] - 13447 < -400:
            self.gripper.start_close()
        else:
            self.gripper.stop()
            
        # TODO: clean up this ugliness
        if vals[3] - 13447 > 400:
            self.lifter.start_lower()
        elif vals[3] - 13447 < -400:
            self.lifter.start_lift()
        else:
            self.lifter.stop()
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self.lifter.run_loop(),
                             self.gripper.run_loop())
        

if __name__ == '__main__':
    claw = Claw()
    asyncio.run(claw.start())
