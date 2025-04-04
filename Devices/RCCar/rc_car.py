#
# RCCar
#
# Version 25_02_02_01
#
from ble_client import BLEClient
from machine import SPI,Pin
import uasyncio as asyncio
from drive_train import DriveTrain
from claw import Claw
from buzzer import Buzzer

class RCCar:
    def __init__(self,
                 left_pins = (10, 11),
                 right_pins = (12, 13),
                 led_pin: int = None,
                 buzzer_pin:int = None,
                 claw: Claw = None)-> None:
        
        # Create Bluetooth client
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=50)
        
        # Create DriveTrain (two motors)
        self.drive_train = DriveTrain(left_pins, right_pins)
        
        # Create additional optional devices
        self.claw = claw
        self.led = None if led_pin is None else Pin(led_pin, Pin.OUT)
        self.buzzer = None if buzzer_pin is None else Buzzer(pin=buzzer_pin)
        
        # RC Car state
        self.running = False
        
    def receive_message(self, message: str)-> str:
        # TODO: clean this up
        #print(f'Message: {message}')
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
        #print(vals)
        left_speed = 100 * (vals[0] - 13447) / 13447
        right_speed = 100 * (vals[2] - 13447) / 13447
        self.drive_train.move(left_speed, right_speed)
        
        if self.claw is not None:
            self.claw.receive_message(message)
        
    def on_connected(self):
        print('Connected')
        if self.led != None:
            self.led.value(1)
        if self.buzzer != None:
            self.buzzer.begin_sound()
            
    def on_disconnected(self):
        print('Disconnected!')
        if self.led != None:
            self.led.value(0)
        if self.buzzer != None:
            self.buzzer.end_sound()
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        if self.claw is None:
            await self.ble_client.run_loop()
        else:
            await asyncio.gather(self.ble_client.run_loop(), self.claw.run_loop()) 
        

if __name__ == '__main__':
    rc_car = RCCar(led_pin=6, buzzer_pin=22, claw=Claw())
    asyncio.run(rc_car.start())
