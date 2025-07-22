#
# Version: 1.00
# Date: 2025-07-09
# Author: Sam Linton
# Description: Interactive control of servos
#
from servo_motor import ServoMotor
# from i2c_servo_motor import I2CServoMotor
# from servo_controller import ServoController
from servo_set import ServoSet
from servo_set_reader import ServoSetReader
# from machine import I2C, Pin


filename: str = 'rear_left_leg.srv'
# filename: str = 'front_right_leg.srv'
#filename: str = 'rear_right_leg.srv'
#filename: str = 'rear_right_leg.srv'

servo_set = ServoSetReader.create_servo_from_file(filename)
servo_set.home()
print(f'Servo Set: {servo_set.name}')

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

        elif command_words[0] in ['?', 'help']:
            print('Commands:')
            print('\th, home: Move to home position')
            print('\ts, start: Move to start position')
            print('\te, end: Move to end position')
            print('\tx, quit, q: Quit the program')
            print('\tangles: Set angles for servos')

        else:
            angles: list[float] = [float(command_word) for command_word in command_words]
            servo_set.set_angles(angles)

        print(f'Logical Angles: {servo_set.get_angles()}')
        print(f'Raw Angles: {servo_set.get_raw_angles()}')

    except Exception as e:
        print(f'Error: {e} Type in servo angles or "x" to quit')
        
    command = input('\nCommand: ')

