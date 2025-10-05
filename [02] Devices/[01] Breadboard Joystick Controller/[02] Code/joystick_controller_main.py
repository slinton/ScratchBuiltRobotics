#
# JoystickController 
# Version 1.00
# Date: 2025-05-30
# Sam Linton
# This script sets up a Bluetooth Low Energy (BLE) server that reads joystick inputs
# and sends them to a connected client. It also controls a buzzer and an LED to indicate    
# connection status.

from ble_server import BLEServer
from machine import Pin, ADC
from buzzer import Buzzer

# Bluetooth connection light
led = Pin(6, Pin.OUT)
led.off()

# Joystick x, y, and button
left_x = ADC(26)
left_y = ADC(27)
right_x = ADC(28)
l_button = Pin(2, Pin.IN, Pin.PULL_UP)
r_button = Pin(3, Pin.IN, Pin.PULL_UP)

# Buzzer
buzzer = Buzzer(pin = 22)

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
    
def create_message():
    """Create a message to send to the connected BLE client."""
    left_x_value = left_x.read_u16()
    left_y_value = left_y.read_u16()
    right_x_value = right_x.read_u16()
    right_y_value = 0
    
    message = f'{left_x_value},{left_y_value},{right_x_value},{right_y_value},{l_button.value()},{r_button.value()}'
    return message


server = BLEServer(
    name = 'BLEServer', # Pick a name for your BLE server
    create_message_func = create_message,
    on_connected_func=connected,
    on_disconnected_func=disconnected,
    send_interval_ms = 100)

server.start()