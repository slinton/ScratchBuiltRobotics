from machine import Pin, I2C
from servo_motor import ServoMotor
from servo_set import ServoSet
from i2c_servo_motor import I2CServoMotor
from pwm_servo_motor import PWMServoMotor
from servo_controller import ServoController

class ServoSetReader:
    servo_controller: ServoController | None = None

    @classmethod
    def create_servo_from_file(cls, filename: str) -> ServoSet:
        with open(filename, 'r') as f:

            # Read the servo set name
            name: str = f.readline().strip()
            print(f"Servo Set Name: {name}")

            servos: list[ServoMotor] = []
            line: str = f.readline().strip()
            while line != '':
                if not line.startswith('#'):
                    words = line.split(',')
                    identifier: str = words[0].strip().lower()

                    if identifier == 'i2c':
                        i2c: I2C = cls.create_i2c_from_line(line)
                        cls.servo_controller = ServoController(i2c)

                    elif identifier == 'i2c servo':
                        servo: ServoMotor = cls.create_i2c_servo_from_line(line, cls.servo_controller)
                        servos.append(servo)

                    elif identifier == 'pwm servo':
                        servo: ServoMotor = cls.create_pwm_servo_from_line(line)
                        servos.append(servo)

                line = f.readline().strip()

        return ServoSet(name=name, servos=servos)

    @classmethod
    def create_i2c_from_line(cls, line: str) -> I2C:
        words = line.split(',')
        if len(words) < 4:
            raise ValueError("Invalid I2C line format")
        
        id: int = int(words[1].strip())
        sda_pin: int = int(words[2].strip())
        scl_pin: int = int(words[3].strip())
        

        return I2C(id=id, sda=Pin(sda_pin), scl=Pin(scl_pin))   

    @classmethod
    def create_i2c_servo_from_line(cls, line: str, controller: ServoController) -> I2CServoMotor:
        words = line.split(',')
        if len(words) < 8:
            raise ValueError("Invalid servo line format")
        
        name: str = words[1].strip()
        pin: int = int(words[2].strip())
        raw_angle_0: float = float(words[3].strip())
        sign: int = int(words[4].strip())
        angle_start: float = float(words[5].strip())
        angle_end: float = float(words[6].strip())
        angle_home: float = float(words[7].strip())
        return I2CServoMotor(
            name=name,
            pin=pin,
            servo_controller=controller,
            raw_angle_0=raw_angle_0,
            sign=sign,
            angle_start=angle_start,
            angle_end=angle_end,
            angle_home=angle_home
        )
    
    @classmethod
    def create_pwm_servo_from_line(cls, line: str) -> PWMServoMotor:
        words = line.split(',')
        if len(words) < 8:
            raise ValueError("Invalid servo line format")
        
        name: str = words[1].strip()
        pin: int = int(words[2].strip())
        raw_angle_0: float = float(words[3].strip())
        sign: int = int(words[4].strip())
        angle_start: float = float(words[5].strip())
        angle_end: float = float(words[6].strip())
        angle_home: float = float(words[7].strip())

        return PWMServoMotor(
            name=name,
            pin=pin,
            raw_angle_0=raw_angle_0,
            sign=sign,
            angle_start=angle_start,
            angle_end=angle_end,
            angle_home=angle_home
        )   


if __name__ == '__main__':
    #import os
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "front_left_leg.srv"
    #full_path = os.path.join(script_dir, filename)
    full_path = filename  # Assuming the file is in the same directory as this script
    print(full_path)
    servo_set: ServoSet = ServoSetReader.create_servo_from_file(full_path)
    servo_set.home()
    print(servo_set)