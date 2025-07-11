#
# Version: 1.00
# Date: 2025-07-09
# Author: Sam Linton
# Description: Interactive control of servos
#
from servo_motor import ServoMotor
from i2c_servo_motor import I2CServoMotor
from servo_controller import ServoController
from servo_set import ServoSet
from machine import I2C, Pin


# Create I2C object
i2c: I2C = I2C(id=1, sda = Pin(14), scl = Pin(15))
print(f'Found {len(i2c.scan())} i2c devices.')
sc: ServoController = ServoController(i2c)

# Create servos and servoset
servos: list[ServoMotor] = [
    I2CServoMotor(
        name='lower-leg', 
        pin = 1, 
        servo_controller = sc, 
        raw_angle_0 = 70, 
        angle_start=0, 
        angle_end=110, 
        angle_home=90),
    I2CServoMotor(
        name='shoulder-forward', 
        pin = 2, 
        servo_controller = sc, 
        raw_angle_0 = 70, 
        angle_start=0, 
        angle_end=90, 
        angle_home=45),
    I2CServoMotor(
        name='shoulder-out',  
        pin = 3, 
        servo_controller = sc, 
        raw_angle_0 = 80, 
        angle_start=-50, 
        angle_end=50, 
        angle_home=0)]
servo_set = ServoSet(servos=servos, name='leg')
servo_set.home()

command = input('\nCommand: ')

while not command.lower() in ['quit', 'q', 'x']:
    try:
        command_words = command.split()
        print(command_words)
        
        if command_words[0] in ['h', 'home']:
            servo_set.move_to_position(servo_set.get_home_position(), time=1.0, num_steps=100)
        elif command_words[0] in ['s', 'start']:
            servo_set.move_to_position(servo_set.get_start_position(), time = 1.0, num_steps = 100)
        elif command_words[0] in ['e', 'end']:
            servo_set.move_to_position(servo_set.get_end_position(), time = 1.0, num_steps = 100)
        else:
            angles: list[float] = [float(command_word) for command_word in command_words]
            servo_set.set_angles(angles)
            
        print(servo_set.get_angles())    
        
    except Exception as e:
        print(f'Error: {e} Type in servo angles or "x" to quit')
        
    command = input('\nCommand: ')
