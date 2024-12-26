# Pinout for Functioning Tests

# Bounding boxes test
demo_bouncing_boxes.py
spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))

# Touch demo
spi0 = SPI(0, baudrate=40_000_000, sck=Pin(18), mosi=Pin(19))
display = Display(spi0, dc=Pin(15), cs=Pin(17), rst=Pin(14))
spi1 = SPI(1, baudrate=1_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

Pins on TFT ILI9341
-------------------
Touch:
-----
T_IRQ	GP0
T_DO	GP12   (SPI1)
T_DIN	GP11   (SPI1)
T_CS	GP3
T_CLK	GP10   (SPI1)T

SDO(MISO)	GP16 (Apparently not used)
LED			VCC
SCK			GP18  (SPI0)
SDI(MOSI)	GP19  (SPI0)
D/C			GP15
RESET		GP14
CS			GP17
GND			GND
VCC			VCC