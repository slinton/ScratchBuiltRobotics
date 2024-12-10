#
# Brain
#
# OBSOLETE?
#
<<<<<<< HEAD
# Version 24_07_31_02
#
=======
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
from ble_client import BLEClient
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import uasyncio as asyncio
from drive_train import DriveTrain
<<<<<<< HEAD
from screen import Screen

# TODO: how to switch from RC mode to Program mode
# TODO: create screen object
# TODO: spi optional

class Brain:
    def __init__(self, left_pins=(10, 11), right_pins=(12, 13), led: int=None)-> None:
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=1000)
        self.running = False
        self.led = None if led == None else Pin(led, Pin.OUT)
        self.drive_train = DriveTrain(left_pins, right_pins)
        self.screen = Screen()
        self.display('Starting...')
        
#     def __init__(self, spi, left_pins, right_pins)-> None:
#         self.ble_client = BLEClient(
#             server_name='JoystickController',
#             receive_message_func=self.receive_message,
#             receive_interval_ms=1000)
#         print(self.ble_client.is_connected())
#         self.running = False
#         self.drive_train = DriveTrain(left_pins, right_pins)
#         self.screen = Screen()
#         self.display('Starting...')
        
#     def create_screen(self, spi, x, y, z):
#         tft = TFT(spi, x, y, z)
#         tft.initr()
#         tft.rgb(True)
#         return tft
    
    def display(self, message: str, color: TFTCOLOR=TFT.WHITE, fontsize: int=1)-> None:
        self.screen.fill(TFT.BLACK)
        self.screen.display(message)
        
    def receive_message(self, message)-> str:
        print(f'Message: {message}')
        #self.display(f'{message}', color=TFT.RED, fontsize=1)
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
        print(vals)
=======

# TODO: how to switch from RC mode to Program mode
# TODO: create screen object

class Brain:
    def __init__(self, spi, left_pins, right_pins)-> None:
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            receive_interval_ms=1000)
        print(self.ble_client.is_connected())
        self.running = False
        self.drive_train = DriveTrain(left_pins, right_pins)
        self.screen = self.create_screen(spi, 16, 17, 18)
        self.screen.fill(TFT.BLACK)
        self.display('Starting...')
        
    def create_screen(self, spi, x, y, z):
        tft = TFT(spi, x, y, z)
        tft.initr()
        tft.rgb(True)
        return tft
    
    def display(self, message: str, color: TFTCOLOR=TFT.WHITE, fontsize: int=1)-> None:
        self.screen.fill(TFT.BLACK)
        self.screen.text((0, 0), message, color, sysfont, fontsize)
        
    def receive_message(self, message)-> str:
#         print(f'Message: {message}')
        #self.display(f'{message}', color=TFT.RED, fontsize=1)
        values = message.split(',')
        vals = (int(values[0], 16), int(values[1], 16), int(values[2], 16), int(values[3], 16), int(values[4]) % 2, int(values[4]) //2)
#         print(vals)
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
        left_speed = 100 * (vals[0] - 13447) / 13447
        right_speed = 100 * (vals[2] - 13447) / 13447
        self.display(f'{left_speed:.0f}% {right_speed:.0f}%', color=TFT.RED, fontsize=1)
        self.drive_train.move(left_speed, right_speed)
<<<<<<< HEAD
        
    def on_connected(self):
        print('Connected')
        if self.led != None:
            self.led.value(1)
            
    def on_disconnected(self):
        print('Disconnected!')
        if self.led != None:
            self.led.value(0)
=======
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
<<<<<<< HEAD
        await self.ble_client.run_loop()
#         while True:
#             #await self.ble_client.update()
#             await self.ble_client.receive_message()
#             await asyncio.sleep_ms(200)
        

if __name__ == '__main__':
#     spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
#               sck=Pin(10), mosi=Pin(11), miso=None)
#     brain = Brain(spi, (1, 2), (3, 4))
    brain = Brain(led=9)
    asyncio.run(brain.start())
    
=======
        while True:
            await self.ble_client.update()
            await asyncio.sleep_ms(200)
        

if __name__ == '__main__':
    spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(10), mosi=Pin(11), miso=None)
    brain = Brain(spi, (1, 2), (3, 4))
    asyncio.run(brain.start())
>>>>>>> 8a7ad559408607d21f58db1b74e8324b7722e05b
