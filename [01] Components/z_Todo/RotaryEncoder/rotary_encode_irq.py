#
# RotaryEncoder
#
# Version 24_07_31_04
#
#
# For some reason this does not work well.
#
from machine import Pin
from time import sleep
import uasyncio as asyncio

def handle_button_down():
    print('.')

class RotaryEncoder:
    def __init__(self, sw, dt, clk)-> None:
        
        self.direction = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.clock = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.change = 'None'
        self.clock.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_rotary_change)
        self.previous = 1

        button = Pin(sw, Pin.IN, Pin.PULL_UP)
        self.button_down = False
        button.irq(handler=self.handle_button_change)
            
    def handle_button_change(self, pin)-> None:
        button_value = pin.value()
        
        if self.button_down and button_value == 1:
            print('button up')
            self.button_down = False
        elif not self.button_down and button_value == 0:
            print('button down')
            self.button_down = True;
            
    def handle_rotary_change(self, pin)-> None:
        if not self.change == 'None':
            return
        
        if self.direction.value() == 0:
            self.change = 'Left'
        else:
            self.change = 'Right'
                
    def print_values(self)-> None:
        print(f'{self.clock.value()} {self.direction.value()} {self.button.value()}')
        
    async def update(self)-> None:
        if not self.change == 'None':
            print(self.change)
            self.change = 'None'
            
    async def run_loop(self)-> None:
        while True:
            await self.update()
            await asyncio.sleep_ms(100)
    
    def start(self)-> None:
        asyncio.run(self.run_loop())


if __name__ == '__main__':
    encoder = RotaryEncoder(sw=13, dt=14, clk=15)
    encoder.start()
    
        
             