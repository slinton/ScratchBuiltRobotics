#
# test_movement
#
from servo_set import ServoSet

if __name__ == "__main__":
    from machine import I2C, Pin
    from servo_controller import ServoController
    from servo_motor import ServoMotor
    from i2c_servo_motor import I2CServoMotor
    from movement import Movement
    
    # Create i2c
    i2c = I2C(id=1, sda=Pin(14), scl=Pin(15))
    
    # Create servo controller
    sc = ServoController(i2c = i2c)

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
            angle_start=-30, 
            angle_end=30, 
            angle_home=0)
    ]
    
    # Create servo set
    servo_set = ServoSet(servos=servos, name = 'test')
    servo_set.home()

    
    home_position = servo_set.get_home_position()
    start_position = servo_set.get_start_position()
    end_position = servo_set.get_end_position()

    movement: Movement = Movement([
        start_position,
        home_position,
        end_position]
    )

    servo_set.execute_movement(movement)