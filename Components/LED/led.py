#
# Led
#
# Version 24_07_31_04
#
# Specify number of blinks
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
        self.index = -1
        self.pin.value(1)
        self.timer.deinit()
        
    def off(self):
        self.index = -1
        self.pin.value(0)
        self.timer.deinit()
        
    def toggle(self):
        self.index = -1
        self.pin.toggle()
        
    def update_index(self):
        self.index += 1
        if self.index >= len(self.periods):
            self.count -= 1
            if self.forever or self.count > 0:
                self.index = 0
            else:
                self.index = -1

        
    def switch(self, timer):
        if self.index < 0:
            self.timer.deinit()
            return
        
        self.pin.toggle()
        period = self.periods[self.index]
#         print(period)
        self.update_index()
        self.timer.init(mode=Timer.ONE_SHOT, period=period, callback=self.switch)
        
    def blink(self, periods=(50, 500), count=-1):
        self.pin.value(0)
        self.index = 0
        self.periods = periods
        self.forever = count == -1
        self.count = count
        self.switch(self.timer)

if __name__ == '__main__':
    try:
        led = Led(pin=9)
        
        print('default blink, turn off after 3 seconds.')
        led.blink()
        sleep(3)
        led.off()
        
        sleep(1)
        print('Repeat sequence two times')
        led.blink(periods=(50, 500), count = 2)
        

        print('blink 4 times')
        for _ in range(4):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)
            
        sleep(2.0)
        print('toggle 4 times')
        for _ in range(4):
            led.toggle()
            sleep(0.5)
            
        print('Auto blink for 5 seconds')
        led.blink()
        sleep(5)
        led.off()
        
        sleep(1)
        print('Blink sequence 1, 2, 3 seconds on, repeated 2 times.')
        led.blink(periods=(1000, 500, 2000, 500, 3000, 500), count=2)
        
        while True:
            sleep(1000)
            pass
        
    except KeyboardInterrupt:
        print('Keyboard interrupt.')
        led.off()
        
