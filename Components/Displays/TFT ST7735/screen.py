#
# Screen
#
# Version 25_03_15
#
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin

# Default pin values:
#
# Pico Pin          SPI / Screen Label  
# 6                 RS
# 7                 RES
# 8                 CS
# 18 (SPI0 SCK)     SCK
# 19 (SPI1 TX)      SDA
# 3.3V              LEDA

class Screen(TFT):
    def __init__(self, spi=None, rs=6, res=7, cs=8)-> None:
        if spi == None:
            spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0,
              sck=Pin(18), mosi=Pin(19), miso=None)
        super().__init__(spi, rs, res, cs);
        self.initr()
        self.rgb(True)
        self.rotation(3)
        self.fill(TFT.BLACK)
        
    def text(self, coords: tuple[int, int], message: str, color: TFTColor = TFT.WHITE, size: int = 1, nowrap: bool = False) -> None:
        super().text(coords, message, color, sysfont, size, nowrap)
        
        
if __name__ == '__main__':
    print('start')
    screen = Screen()
    width, height = screen.size()
    y = width / 2
    screen.fill()
    screen.text((0, y), "Want pi?", TFT.GREEN)
    screen.line((0, 0), (width, height), TFT.RED)
    

