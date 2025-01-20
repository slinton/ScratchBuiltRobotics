#
# Gripper Assembly
#
# Version 25_01_19_01
#
from ble_client import BLEClient
from machine import SPI,Pin
import uasyncio as asyncio
from gripper import Gripper
from lifter import Lifter
from time import sleep

class GripperAssembly:
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
        #self.gripper.close()
        self.lifter.lift()
        sleep(0.5)
       
    def receive_message(self, message)-> str:
        #print(f'Message: {message}')
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
        print(vals)
        
        if vals[4] == 1:
            self.lifter.lift()
        elif vals[5] == 1:
            self.lifter.lower()
            
        lifter_angle_change = 0
        if vals[3] - 13447 > 400:
            lifter_angle_change = 10
        elif vals[3] - 13447 < -400:
            lifter_angle_change = -10
        #gripper_angle_change = GripperAssembly.gain * (vals[1] - 13447) / 13447
        #lifter_angle_change = GripperAssembly.gain * (vals[3] - 13447) / 13447
        print(f'----- {lifter_angle_change}')
        self.lifter.move_by(lifter_angle_change)
        #lifter.set_angle(
        
    def on_connected(self):
        print('Connected')
            
    def on_disconnected(self):
        print('Disconnected!')
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await self.ble_client.run_loop()
        

if __name__ == '__main__':
    gripper_assembly = GripperAssembly()
    asyncio.run(gripper_assembly.start())
    
        
        
    
        
        
        



