#
# Screen
#
# Version 24_07_31_00
#
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin

# TODO:
# Create Screen base class to quickly switch between screen types
# Default pin values:
#
# Pico Pin          SPI / Screen Label  
# 6                 RS
# 7                 RES
# 8                 CS
# 18 (SPI0 SCK)     SCK
# 19 (SPI1 TX       SDA

class Screen:
    def __init__(self, spi=None, rs=6, res=7, cs=8)-> None:
        if spi == None:
            spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0,
              sck=Pin(18), mosi=Pin(19), miso=None)
        self.screen = TFT(spi, rs, res, cs)
        self.screen.initr()
        self.screen.rgb(True)
        self.screen.rotation(3)
        self.screen.fill(TFT.BLACK)
        self.dimensions = (128, 160)
        
    def size(self) :
        return self.screen.size()
    
    def fill(self, color: TFTCOLOR=TFT.BLACK):
        self.screen.fill(TFT.BLACK)
        
    def display(self, message: str, position=(0, 0), color: TFTCOLOR=TFT.WHITE, fontsize: int=1)-> None:
        self.screen.text(position, message, color, sysfont, fontsize)
        
        
if __name__ == '__main__':
    screen = Screen()
    y = screen.size()[1] / 2
    screen.fill()
    screen.display('Hello, World!', position = (30, y))
    
        
