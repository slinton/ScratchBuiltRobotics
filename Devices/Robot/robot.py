#
# Robot
#
# Remote control or autonomous robot

# Version 25_03_09_01
#
# Consider: change JoystickController output to -100 to 100 for speed
#
from ble_client import BLEClient
from machine import Pin
import uasyncio as asyncio
from drive_train import DriveTrain
from claw import Claw
from buzzer import Buzzer
from time import sleep

class Robot:
    def __init__(self,
                 left_pins = (10, 11),
                 right_pins = (12, 13),
                 led_pin: int = None,
                 buzzer_pin: int = None,
                 claw: Claw | None = None)-> None:
        
        # Autonomous or remote control mode
        self.autonomous: bool = False
        
        # Create Bluetooth client
        self.ble_client: BLEClient = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=50)
        
        # Create DriveTrain (two motors)
        self.drive_train: DriveTrain = DriveTrain(left_pins, right_pins)
        
        # Create additional optional devices
        self.claw: Claw | None = claw
        self.led: Pin | None = None if led_pin is None else Pin(led_pin, Pin.OUT)
        self.buzzer: Buzzer | None = None if buzzer_pin is None else Buzzer(pin=buzzer_pin)
        
        # RC Car state
        self.running: bool = False
        
    def receive_message(self, message: str)-> None:
        """Function to run when a message is received from the BLE server.

        Args:
            message (str): message from the JoystickController
        """

        # Parse the message
        vals: tuple[int, int, int, int, int, int] = self.get_values(message)

        # Toggle autonomous mode
        if vals[4] == 1 and vals[5] == 1:
            self.autonomous = not self.autonomous

        if self.autonomous:
            print('Autonomous mode')
            # Start autonomous mode
            self.run_autonomous()
            self.autonomous = False
            exit()
            return

        # Calculate the speed of the left and right motors
        left_speed = 100 * (vals[0] - 13447) / 13447
        right_speed = 100 * (vals[2] - 13447) / 13447
        self.drive_train.move(left_speed, right_speed)
        
        if self.claw is not None:
            self.claw.receive_message(message)

    def get_values(self, message: str)-> tuple:
        """Get the values from the message.

        Args:
            message (str): message from the JoystickController

        Returns:
            tuple: values from the message
        """
        values = message.split(',')
        vals = (int(values[0], 16), 
                int(values[1], 16), 
                int(values[2], 16), 
                int(values[3], 16), 
                int(values[4]) % 2, 
                int(values[4]) //2)
        return vals
        
    def on_connected(self):
        """Function to run when the BLE connection is established.
        """
        print('Connected')
        if self.led != None:
            self.led.value(1)
        if self.buzzer != None:
            self.buzzer.begin_sound()
            
    def on_disconnected(self):
        """Method to run when the BLE connection is lost.
        """
        print('Disconnected!')
        if self.led != None:
            self.led.value(0)
        if self.buzzer != None:
            self.buzzer.end_sound()

    def run_autonomous(self)-> None:
        """Method to run the robot in autonomous mode.
        """
        # Read and run run_code.py if it exists
        try:
            with open('run_code.py', 'r') as f:
                code = f.read()
                exec(code, {'robot': self})  
        except OSError:
            print('No run_code.py file found!')
            return

    def move(self, left_speed: int, right_speed: int, time_sec: float)-> None:
        """Arbitrary motion, controlling the speed of each motor independently.

        Args:
            left_speed (int): speed of the robot in the range -100 to 100
            right_speed (int): speed of the robot in the range -100 to 100
            time_sec (float): number of seconds
        """
        self.drive_train.move(left_speed, right_speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def forward(self, speed: int, time_sec: float)-> None:
        """Drive the robot forward at a given speed.

        Args:
            speed (int): speed of the robot in the range (-100, +100)
            time_sec (float): number of seconds
        """
        
        self.drive_train.forward(speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def backward(self, speed: int, time_sec: float)-> None:
        """Drive the robot backward at a given speed.

        Args:
            speed (int): backwards speed of the robot in the range (-100, +100)
            time_sec (float): number of seconds
        """
        
        self.drive_train.backward(speed)
        sleep(time_sec)
        self.drive_train.stop()
    
    def turn_left(self, speed: int, time_sec: float)-> None:
        """Turn the robot left at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
            time_sec (float): number of seconds
        """
        
        self.drive_train.turn_left(speed)
        sleep(time_sec)
        self.drive_train.stop()
        
    def turn_right(self, speed: int, time_sec: float)-> None:
        """Turn the robot right at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
            time_sec (float): number of seconds
        """
        
        self.drive_train.turn_right(speed)
        sleep(time_sec)
        self.drive_train.stop()

    def start(self)-> None:
        """Method to start the robot running
        """
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        if self.claw is None:
            await self.ble_client.run_loop()
        else:
            await asyncio.gather(self.ble_client.run_loop(), self.claw.run_loop()) 
        

if __name__ == '__main__':
    robot = Robot(led_pin=6, buzzer_pin=22, claw=Claw())
    asyncio.run(robot.start())
