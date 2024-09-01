#
# Brain
#
from ble_client import BLEClient
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import uasyncio as asyncio

# TODO: how to switch from RC mode to Program mode

class Brain:
    def __init__(self, spi)-> None:
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            receive_interval_ms=1000)
        print(self.ble_client.is_connected())
        self.running = False
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
        print(f'Message: {message}')
        self.display(f'{message}', color=TFT.RED, fontsize=1)
        values = message.split(',')
        vals = (int(values[0], 16), int(values[0], 16), int(values[0], 16), int(values[0], 16), int(values[4]) % 2, int(values[4]) //2)
        print(vals)
        
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        while True:
            await self.ble_client.update()
            await asyncio.sleep_ms(1000)
        

if __name__ == '__main__':
    spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(10), mosi=Pin(11), miso=None)
    brain = Brain(spi)
    asyncio.run(brain.start())
    
        
        
    
        
        
        
