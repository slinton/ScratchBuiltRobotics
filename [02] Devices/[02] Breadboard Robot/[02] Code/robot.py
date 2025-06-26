#
# robot
#
# Version: 1.00
# Date: 2025-05-30
# Author Sam Linton
# Description: This script controls a robot that is controlled with 
# Bluetooth Low Energy (BLE) using a BBJoystickController. 
# The robot has two motors, a buzzer, and (optionally) a launcher.
# The robot uses tank-drive with two joysticks.
#
from ble_client import BLEClient
from machine import Pin, PWM
from buzzer import Buzzer
from servo import Servo
from time import sleep

# Motor control
LOW = 0
HIGH = 65_535
freq = 20_000

# Left Motor: OUT1 and OUT2
left_1 = PWM(Pin(10, Pin.OUT), freq) # 14
left_2 = PWM(Pin(11, Pin.OUT), freq) # 15

# Right Motor: OUT3 and OUT4
right_1 = PWM(Pin(12, Pin.OUT), freq) # 16
right_2 = PWM(Pin(13, Pin.OUT), freq) # 17

# Connection led
led = Pin(6, Pin.OUT)
led.off()

# Buzzer
buzzer = Buzzer(pin = 22)

# Launcher (optional)
launcher = Servo(pin_id = 16)
launcher.write(180)

def connected():
    """Callback function when a BLE connection is established."""
    print('CONNECTED')
    led.on()
    buzzer.begin_sound()
    
def disconnected():
    """Callback function when a BLE connection is disconnected."""
    print('DISCONNECTED')
    led.off()
    buzzer.end_sound()
    
def launch():
    """Launch the robot's launcher."""
    print('Launch!')
    launcher.write(30)
    sleep(0.5)
    launcher.write(180)
    
def get_speed(value):
    """Convert joystick value to motor speed."""
    speed = 2 * value - HIGH
    if abs(speed) < 5000:
        speed = 0
    return speed
               
def move(left_speed, right_speed):
    """Move the robot based on the left and right speed values.

    Args:
        left_speed (int): left wheel speed
        right_speed (int): right wheel speed
    """
    if left_speed > 0:
        left_1.duty_u16(left_speed)
        left_2.duty_u16(0)
    else:
        left_1.duty_u16(0)
        left_2.duty_u16(-left_speed)
            
    if right_speed > 0:
        right_1.duty_u16(right_speed)
        right_2.duty_u16(0)
    else:
        right_1.duty_u16(0)
        right_2.duty_u16(-right_speed)

def receive_message(message):
    """Receive a message from the BLE client and interpret it to 
    control the robot."""
    values = message.split(',')
    left_x_value = int(values[0])
    left_y_value = int(values[1])
    right_x_value = int(values[2])
    right_y_value = 0
    left_button = int(values[4])
    right_button = int(values[5])
    if left_button == 0:
        launch()
    
    # Two joysticks, tank-drive
    left_speed = get_speed(left_x_value) # 2 * left_value - HIGH
    right_speed = get_speed(right_x_value)
    
    print(f'{left_x_value},{left_y_value},{right_x_value},{right_y_value},{left_button},{right_button}')
    move(left_speed, right_speed)

    
client = BLEClient(
    server_name='BLEServer', # Must match the name of the JoystickController 
    on_connected_func=connected,
    on_disconnected_func=disconnected,
    receive_message_func=receive_message,
    receive_interval_ms=100)

client.start()

