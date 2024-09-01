#
# RotaryEncoder
# Version 0.1
#
from machine import Pin
from time import sleep
import uasyncio as asyncio


class RotaryEncoder:
    def __init__(self,
                 sw,
                 dt,
                 clk,
                 on_button_down_func=None,
                 on_button_up_func=None,
                 on_left_func=None,
                 on_right_func=None)-> None:
        """Initialize the RotaryEncoder class.

        Args:
            sw (int): Button (SW) pin number
            dt (int): DT pin number
            clk (int): CLK pin number
            on_button_down_func (Callable, optional): Function to call when button down. Defaults to None.
            on_button_up_func (Callable, optional): Function to call when button up. Defaults to None.
            on_left_func (Callable, optional): Function to call when rotary turned left. Defaults to None.
            on_right_func (Callable, optional): Function to call when rotary turned right. Defaults to None.
        """
        
        # Rotary encoder part
        self.direction = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.clock = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.previous = 1
        self.on_left_func = on_left_func
        self.on_right_func = on_right_func
    
        # Button part
        self.button = Pin(sw, Pin.IN, Pin.PULL_UP)
        self.button_down = False
        self.on_button_down_func = on_button_down_func
        self.on_button_up_func = on_button_up_func

        
    def print_values(self)-> None:
        """Print the values of the rotary encoder and button.
        """
        print(f'{self.clock.value()} {self.direction.value()} {self.button.value()}')
        
    def on_rotary_left(self)-> None:
        """Call the function associated with the left turn of the rotary encoder.
        """
        if self.on_left_func:
            self.on_left_func()
        else:
            print('LEFT')
    
    def on_rotary_right(self)-> None:
        """Call the function associated with the right turn of the rotary encoder.
        """
        if self.on_right_func:
            self.on_right_func()
        else:
            print('RIGHT')
    
    def on_button_down(self)-> None:
        """Call the function associated with the button down event.
        """
        if self.on_button_down_func:
            self.on_button_down_func()
        else:
            print('DOWN')
    
    def on_button_up(self)-> None:
        """Call the function associated with the button up event.
        """
        if self.on_button_down_func:
            self.on_button_down_func()
        else:
            print('UP')
        
    async def update(self)-> None:
        """Update the rotary encoder and button values.
        """
        # Rotary encoder part
        current = self.clock.value()
        direct = self.direction.value()
        if current != self.previous:
            if current == 0:
                if direct == 0:
                    self.on_rotary_left()
                   
                else:
                    if self.on_right_func:
                        self.on_right_func()
            self.previous = current
            
        # Button part
        button_value = self.button.value()
        if self.button_down and button_value == 1:
            print('UP')
            self.button_down = False
        elif not self.button_down and button_value == 0:
            print('DN')
            self.button_down = True
            
    async def run_loop(self)-> None:
        """Loop to run the rotary encoder and button functions.
        """
        while True:
            await self.update()
    
    def start(self)-> None:
        """Syncronous method to start the rotary encoder and button functions."""
        asyncio.run(self.run_loop())


if __name__ == '__main__':
    encoder = RotaryEncoder(
        sw=13,
        dt=14,
        clk=15,
        on_left_func = lambda: print('Left'),
        on_right_func = lambda: print('Right'),
        on_button_down_func = lambda: print('Down'),
        on_button_up_func = lambda: print('Up')
        )
    encoder.start()
    
        
             