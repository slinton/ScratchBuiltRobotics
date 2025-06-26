from machine import Pin, PWM
from time import sleep

freq = 20_000
MAX_DUTY_CYCLE: int = 65535

# OUT1 and OUT2
left_1 = PWM(Pin(10, Pin.OUT), freq) # 14
left_2 = PWM(Pin(11, Pin.OUT), freq) # 15

while True:
    # Forward
    print('forward')
    left_1.duty_u16(MAX_DUTY_CYCLE)
    left_2.duty_u16(0)
    sleep(1)
    
    # Stop
    print('stop')
    left_1.duty_u16(0)
    left_2.duty_u16(0)
    sleep(1)
    
    # Backwards
    print('backwards')
    left_1.duty_u16(0)
    left_2.duty_u16(MAX_DUTY_CYCLE)
    sleep(1)
    
    # Stop
    print('stop')
    left_1.duty_u16(0)
    left_2.duty_u16(0)
    sleep(1)