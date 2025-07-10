#from servo_motor import ServoMotor

def read_servo_from_file(filename: str) -> str:
    with open(filename, 'r') as f:
        servo_values: str = f.readline()
        print(servo_values)
    

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "leg.srv"
    full_path = os.path.join(script_dir, filename)
    print(full_path)
    read_servo_from_file(full_path)