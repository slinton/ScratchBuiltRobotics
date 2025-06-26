#
# RCClaw
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: Radio-controlled claw using a BLE client to receive messages from a joystick controller.
# TODO: Refactor:
# Claw class that only takes lifter/gripper commands, and
# Separate test classes, one including BLEClient and one without.
#
from ble_client import BLEClient
import uasyncio as asyncio
from gripper import Gripper
from lifter import Lifter
from time import sleep

class RCClaw:
    gain: float = 30.0
    
    def __init__(self, gripper_pin: int = 17, lifter_pin: int = 16)-> None:
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=50) #50
        self.running = False
        self.gripper = Gripper(pin=gripper_pin)
        self.lifter = Lifter(pin=lifter_pin)
        
        sleep(0.5)
        self.gripper.close()
        self.lifter.lift()
        sleep(0.5)
       
    def receive_message(self, message)-> str:
        #print(f'Message: {message}')
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
        #print(vals)
        
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
        
    def on_connected(self):
        print('Connected')
            
    def on_disconnected(self):
        print('Disconnected!')
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self.ble_client.run_loop(),
                             self.lifter.run_loop(),
                             self.gripper.run_loop())
        

if __name__ == '__main__':
    rc_gripper_assembly = RCClaw()
    rc_gripper_assembly.start()