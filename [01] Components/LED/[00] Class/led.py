#
# Led
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A LED class for Raspberry Pi Pico that allows blinking with specified patterns and counts.
#
# TODO: Rewrite this using asyncio for better control and non-blocking behavior.
# 
from machine import Pin, Timer
from time import sleep
import uasyncio as asyncio


class Led:
    UNLIMITED = -1
    
    def __init__(self, pin=6):
        self.pin = Pin(pin, Pin.OUT)
        self.timer = Timer()
        self.periods = None
        self.index = -1
        self.forever = False # Repeat the pattern forever
        self.count = 0       # Number of times to repeat pattern
        
    def on(self):
        """Turn the LED on."""
        self.index = -1
        self.pin.value(1)
        self.timer.deinit()
        
    def off(self):
        """Turn the LED off."""
        self.index = -1
        self.pin.value(0)
        self.timer.deinit()
        
    def toggle(self):
        """Toggle the LED state."""
        self.index = -1
        self.pin.toggle()
        
    def _update_index(self):
        """Private method to update the index for cycling through the blink pattern."""
        self.index += 1
        if self.index >= len(self.periods):
            self.count -= 1
            if self.forever or self.count > 0:
                self.index = 0
            else:
                self.index = -1

    def _switch(self, timer):
        """Private function to start the LED blinking."""
         # If index is negative, stop the timer
         # This happens when the count reaches zero or the pattern ends
        if self.index < 0:
            self.timer.deinit()
            return
        
        self.pin.toggle()
        period = self.periods[self.index]
        self._update_index()
        self.timer.init(mode=Timer.ONE_SHOT, period=period, callback=self._switch)
        
    def blink(self, periods=(50, 500), count=-1):
        """Blink the LED with specified periods and count.
        This method will toggle the LED on and off according to the specified periods.

        Args:
            periods (tuple, optional): LED on and off times (seconds). Defaults to (50, 500).
                The first value is the time the LED is on, and the second value is the time it is off.
                If more than two values are provided, the LED will cycle through them.
            count (int, optional): number of times to repeat the specified periods. 
                Defaults to -1, which means repeat forever.
        """
        self.pin.value(0)
        self.index = 0
        self.periods = periods
        self.forever = count == -1
        self.count = count
        self._switch(self.timer)


if __name__ == '__main__':
    try:
        led = Led(pin=6)

        # Test basic on/off functionality
        print('Test basic blink 4 times', end='')
        for _ in range(4):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)
        print('done.')
        sleep(2)

        # Test toggle functionality
        print('Test toggle 4 times', end='')
        for _ in range(4):
            led.toggle()
            sleep(0.5)
        print('done.')
        sleep(2)
        
        # Test default blink
        print('Test default blink, turn on for 3 seconds...', end='')
        led.blink()
        sleep(3)
        led.off()
        print('done.')
        sleep(2)

        # Test blink with custom periods
        print('Test blink with specified periods (50, 500)...', end='')  
        led.blink(periods=(50, 500), count = 2)
        print('done.')
        sleep(2)

        # Test auto blink
        print('Auto blink for 5 seconds', end='')
        led.blink()
        sleep(5)
        led.off()
        print('done.')
        sleep(2)
        
        # Test blink with multiple periods
        print('Blink sequence 1, 2, 3 seconds on, repeated 2 times.', end='')
        led.blink(periods=(1000, 500, 2000, 500, 3000, 500), count=2)
        sleep(10)  # Wait for the blink sequence to complete
        print('done.')
        led.off()
        
        print('All tests completed.')
        
    except KeyboardInterrupt:
        print('Keyboard interrupt.')
        led.off()
        
