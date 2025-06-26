#
# servo_explorer
#
# V2025_02_12_01
#
from servo_info import ServoInfo
from servo_set import ServoSet
from machine import I2C
from time import sleep

# Create I2C object
i2c = I2C(0, sda=0, scl=1)
print(f'Found {len(i2c.scan())} i2c devices.')

# Create servo info objects
servo_infos = [ServoInfo(0, 0, 180), ServoInfo(1, 0, 180), ServoInfo(2, 0, 180)]
servo_set = ServoSet(i2c, servo_infos)

servo_index = 0

command = input('\nCommand: ')

while not command.lower() in ['quit', 'q', 'x']:
    try:
        command_words = command.split()
        if command_words[0].strip() == '?':
            angle = servo_set.read(servo_index)
            print(f'Servo {servo_index}: {angle}')
            
        elif len(command_words) == 2 and command_words[0].strip() == 's':
            servo_index = int(command_words[1])
            angle = servo_set.read(servo_index)
            print(f'Servo {servo_index}: {angle}')
            
        else:
            for command_word in command_words:
                angle = float(command_word)
                print(f'Servo {servo_index}: {angle}')
                servo_set.write(servo_index, angle)
                sleep(0.5)
        
    except Exception as e:
        print(f'Command could not be interpreted. {e} Should be of form "index angle" or "x" to quit')
        
    command = input('\nCommand: ')
