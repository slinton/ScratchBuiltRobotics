#
# Gripper
#
# Version 25_01_19_01
#
#
from servo import Servo
from time import sleep

class Gripper:
    """Implement the gripper
    """

    def __init__(self, pin: int=17, servo_close_angle: float = 70.0, servo_open_angle: float=160.0, ) -> None:
        """Initializer

        Gripper angle goes from 0 (closed) to open_angle (fully open)
        These angles correspond with the servo_close_angle and servo_open_angle, respectively

        Args:
            pin (int, optional): pin for the gripper PWM signal. Defaults to 16.
            open_angle (float, optional): Angle in degrees corresponding to open gripper. Defaults to 160.0.
            close_angle (float, optional): Angle in degrees corresponding to closed gripper. Defaults to 70.0.
        """
        self.servo: Servo = Servo(pin_id=pin)
        self.servo_close_angle: float = servo_close_angle
        self.servo_open_angle: float = servo_open_angle
        self.close_angle: float = 0.0
        self.open_angle: float = abs(self.servo_open_angle - self.servo_close_angle)
        self.sign: float = 1 if self.servo_open_angle > self.servo_close_angle else -1
        self.angle: float | None = None
        
    def open(self, time:float = None) -> None:
        """Open the gripper completely
        """
        if time == None or self.angle == None:
            self.set_angle(self.open_angle)
        else:
            self.move(self.angle, self.open_angle, time)
        
        
    def close(self, time: float = None) -> None:
        """Close the gripper completely
        """
        if time == None or self.angle == None:
            self.set_angle(self.close_angle)
        else:
            self.move(self.angle, self.close_angle, time)
            
    def move_by(self, d_angle: float) -> None:
        """Move the gripper by the angle increment given. Open direction is +

        Args:
            d_angle (float): requested change in angle (degrees)
        """
                
        if self.angle == None: return
        new_angle = self.angle + d_angle
        if self.close_angle < new_angle < self.open_angle:
            self.set_angle(new_angle)

    def move_to(self, end_angle: float, time: float, num_angles:int = 10):
        """Move from the current angle to the end angle (in degrees) in the given amount of
        time (in seconds). 

        Args:
            end_angle (float): Ending angle of the motion, degrees
            time (float): time in which to make the motion, in seconds
            num_angles (int, optional): Number of steps to take. Defaults to 10.
        """
        self._move(self.angle, end_angle, time, num_angles)
        
    def _move(self, start_angle: float, end_angle: float, time: float, num_angles:int = 10):
        """Move from the start angle to the end angle (in degrees) in the given amount of
        time (in seconds). 
        Caution: if the start_angle is not the current angle, this will start with an abrupt
        movement to the start_angle

        Args:
            start_angle (float): Starting angle of the motion, degrees
            end_angle (float): Ending angle of the motion, degrees
            time (float): time in which to make the motion, in seconds
            num_angles (int, optional): Number of steps to take. Defaults to 10.
        """
        d_angle: float = (end_angle - start_angle) / (num_angles - 1)
        d_time: float = time / (num_angles - 1)
    
        for i in range(num_angles):
            angle: float = start_angle + i * d_angle
            print(angle)
            self.set_angle(angle)
            sleep(d_time)

    def get_angle(self) -> float:
        """Get current angle in degrees. This will be None when starting out.

        Returns:
            float: current angle in degrees
        """
        return self.angle
        
    def set_angle(self, angle: float) -> None:
        """Set angle of gripper. O represents closed.

        Args:
            angle (float): angle of gripper. 
        """
        servo_angle: float = self.servo_close_angle + self.sign * angle
        self._set_servo_angle(servo_angle=servo_angle)
        self.angle = angle
        
    def _set_servo_angle(self, servo_angle: float) -> None:
        """Helper function to set servo angle based

        Args:
            servo_angle (float): servo angle in degrees
        """
        servo_angle: float = min(self.servo_open_angle, max(self.servo_close_angle, servo_angle))
        print(f'Gripper servo angle = {servo_angle}')
        self.servo.write(servo_angle)
        
        
if __name__ == '__main__':
    gripper = Gripper()
    gripper.close()
    sleep(0.5)
    
    
#     for _ in range(5):
#         gripper.open()
#         sleep(1)
#         gripper.close()
#         sleep(1)
#     gripper.open()
#     sleep(2)

    num_angles: int = 100
    max_angle: float = 90.0
    time: float = 3.0
    d_angle: float = max_angle / (num_angles-1)
    print(f'd_angle = {d_angle}')
    d_time: float = time / (num_angles-1)
    
    for i in range(num_angles):
        angle: float = i * d_angle
        print(angle)
        gripper.set_angle(angle)
        sleep(d_time)
        
    
