# MatrixDisplay
# https://github.com/stechiez/raspberrypi-pico/tree/main/pico_max7219
#
# mosi = DIN
# 
import max7219
from machine import Pin, SPI
from time import sleep
import framebuf

spi = SPI(0, baudrate=10_000_000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT) # CS

msg = 'STechiezDIY'
length = len(msg)
length = (length*8)
display = max7219.Matrix8x8(spi, ss, 1) # Last number is number of 8x8's in a chain
display.brightness(1)   # adjust brightness 1 to 15
display.fill(0)
display.show()
sleep(0.5)

smile = [
        0b00000000,
        0b01100110,
        0b01100110,
        0b00000000,
        0b00000000,
        0b01000010,
        0b00111100,
        0b00000000
        ]
frown = [
        0b00000000,
        0b01100110,
        0b01100110,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00111100,
        0b01000010
        ]
neutral = [
        0b00000000,
        0b01100110,
        0b01100110,
        0b00000000,
        0b00000000,
        0b00000000,
        0b01111110,
        0b00000000
        ]
suprise = [
        0b00000000,
        0b01100110,
        0b01100110,
        0b00000000,
        0b00111100,
        0b00100100,
        0b00111100,
        0b00000000
        ]

def do_expr(bits):
    buffer = bytearray(bits)
    fbuf = framebuf.FrameBuffer(buffer, 8, 8, framebuf.MONO_HLSB)
    display.blit(fbuf, 0, 0)
    display.show()
    
while True:
    do_expr(smile)
    sleep(0.5)
    do_expr(neutral)
    sleep(0.5)
    do_expr(frown)
    sleep(0.5)
    do_expr(neutral)
    sleep(0.5)
    do_expr(suprise)
    sleep(0.5)
    do_expr(neutral)
    sleep(0.5)

# display.fill(1)
# display.framebuf.pixel(4, 4, 1)
# display.text(msg, 16, 0, 1)
# display.rect(4, 4, 2, 2, 1)
# display.show()


# while True:
#     sleep(1.0)
#     display.scroll(1, 0)
#     display.show()

# while True:
#     for x in range(32, -length, -1):
#         display.text(msg ,x,0,1)
#         display.show()
#         sleep(0.10)
#         display.fill(0)
# display.line(1, 1, 5, 5, 1)
# while True:
#     display.text('hi', 32, 0, 1)
#     display.show()
#     sleep(0.1)
