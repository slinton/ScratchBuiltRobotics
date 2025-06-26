#
# This is sample code to go along with the ST7735 library
#

# Default pin values:
#
# Pico Pin          SPI / Screen Label  
# 6                 RS
# 7                 RES
# 8                 CS
# 18 (SPI0 SCK)     SCK
# 19 (SPI1 TX)      SDA
# 3.3V              LEDA
#
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import time
import math

# Pins
rs = 6
res = 7
cs = 8

# Create SPI bus
spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0,
              sck=Pin(18), mosi=Pin(19), miso=None)

# Create tft display
tft = TFT(spi, rs, res, cs)

# Initialize
tft.initr()
tft.rgb(True)

def test_lines(color) -> None:
    width, height = tft.size()
    
    tft.fill(TFT.BLACK)
    for x in range(0, width, 6):
        tft.line((0,0),(x, height - 1), color)
    for y in range(0, height, 6):
        tft.line((0,0),(width - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, width, 6):
        tft.line((height - 1, 0), (x, height - 1), color)
    for y in range(0, height, 6):
        tft.line((width - 1, 0), (0, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, width, 6):
        tft.line((0, height - 1), (x, 0), color)
    for y in range(0, height, 6):
        tft.line((0, height - 1), (width - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, width, 6):
        tft.line((width - 1, height - 1), (x, 0), color)
    for y in range(0, height, 6):
        tft.line((width - 1, height - 1), (0, y), color)

def test_fast_lines(color1, color2):
    width, height = tft.size()
    
    tft.fill(TFT.BLACK)
    for y in range(0, height, 5):
        tft.hline((0, y), width, color1)
    for x in range(0, width, 5):
        tft.vline((x, 0), height, color2)

def test_draw_rects(color):
    width, height = tft.size()
    
    tft.fill(TFT.BLACK);
    for x in range(0, width, 6):
        tft.rect((width // 2 - x // 2, height // 2 - x / 2), (x, x), color)

def test_fill_rects(color1, color2):
    width, height = tft.size()
    
    tft.fill(TFT.BLACK);
    for x in range(width, 0, -6):
        tft.fillrect((width // 2 - x // 2, height // 2 - x / 2), (x, x), color1)
        tft.rect((width // 2 - x // 2, height // 2 - x / 2), (x, x), color2)


def test_fill_circles(radius, color):
    width, height = tft.size()
    
    for x in range(radius, width, radius * 2):
        for y in range(radius, height, radius * 2):
            tft.fillcircle((x, y), radius, color)

def test_draw_circles(radius, color):
    width, height = tft.size()
    
    for x in range(0, width + radius, radius * 2):
        for y in range(0, height + radius, radius * 2):
            tft.circle((x, y), radius, color)

def test_triangles():
    tft.fill(TFT.BLACK);
    color = 0xF800
    w = tft.size()[0] // 2
    x = tft.size()[1] - 1
    y = 0
    z = tft.size()[0]
    for t in range(0, 15):
        tft.line((w, y), (y, x), color)
        tft.line((y, x), (z, x), color)
        tft.line((z, x), (w, y), color)
        x -= 4
        y += 4
        z -= 4
        color += 100

def test_round_rects():
    tft.fill(TFT.BLACK);
    color = 100
    for t in range(5):
        x = 0
        y = 0
        w = tft.size()[0] - 2
        h = tft.size()[1] - 2
        for i in range(17):
            tft.rect((x, y), (w, h), color)
            x += 2
            y += 3
            w -= 4
            h -= 6
            color += 1100
        color += 100

def tft_print_test():
    tft.fill(TFT.BLACK);
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, sysfont, 2, nowrap=True)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)
    time.sleep_ms(1500)
    tft.fill(TFT.BLACK);
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Want pi?", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Print HEX!", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " seconds.", TFT.WHITE, sysfont)

def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", TFT.WHITE, sysfont, 1)
    time.sleep_ms(200)

    tft_print_test()
    time.sleep_ms(4000)

    test_lines(TFT.YELLOW)
    time.sleep_ms(500)

    test_fast_lines(TFT.RED, TFT.BLUE)
    time.sleep_ms(500)
 
    test_draw_rects(TFT.GREEN)
    time.sleep_ms(500)
 
    test_fill_rects(TFT.YELLOW, TFT.PURPLE)
    time.sleep_ms(500)
 
    tft.fill(TFT.BLACK)
    test_fill_circles(10, TFT.BLUE)
    test_draw_circles(10, TFT.WHITE)
    time.sleep_ms(500)
 
    test_round_rects()
    time.sleep_ms(500)

    test_triangles()
    time.sleep_ms(500)

test_main()



