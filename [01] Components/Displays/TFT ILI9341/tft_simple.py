from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont


spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
display.clear()

# Load sprite
sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
display.draw_sprite(sprite, 50, 70, 41, 49)

display.draw_image('images/RaspberryPiWB128x128.raw', 100, 100, 128, 128)

size = 20
display.fill_hrect(20, 30, size, size, color565(255, 0, 0))

display.draw_hline(10, 319, 229, color565(255, 0, 255))

display.draw_vline(10, 0, 319, color565(0, 255, 255))

display.draw_hline(0, 0, 222, color565(255, 0, 0))

display.draw_line(127, 0, 64, 127, color565(255, 255, 0))

arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
display.draw_text(0, 255, 'Arcade Pix 9x11', arcadepix,
                      color565(255, 0, 0),
                      landscape=True)

