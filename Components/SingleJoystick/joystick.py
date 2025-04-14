#
#
#
from machine import Pin, ADC
from time import sleep
from ble_server import BLEServer

BLE_PIN = 6
BUTTON_PIN = 2
X_PIN = 26
Y_PIN = 27

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
x = ADC(X_PIN)
y = ADC(Y_PIN)
ble = Pin(BLE_PIN, Pin.OUT)

def create_message():
    button_value = 1 - self.left_button.value()
    message = f'{x.value()},{y.value()},{button.value()}'
    return message
    
def on_connected():
    print('connected')
    
def on_disconnected():
    print('disconnected')
    

if __name__ == '__main__':
    try:
        joystick_controller = BLEServer(
            name='JoystickController',
            create_message_func = create_message,
            on_connected_func=on_connected,
            on_disconnected_func=on_disconnected,
            send_interval_ms=100)
        joystick_controller.start()
    
    except KeyboardInterrupt:
        print('Program terminated')
    