#
# Gripper
#
# Version 25_01_19_01
#
# Gripper part only.
#
from servo import Servo

class Lifter:
    """Implement the gripper lifter mechanism
    """

    def __init__(self,
                 pin: int=16,
                 servo_top_angle: float = 0.0,
                 servo_bottom_angle: float=180.0,
                 ) -> None:
        """Initializer

        Gripper lifter angle goes from 0 (closed) to open_angle (fully open)
        These angles correspond with the servo_top_angle and servo_bottom_angle, respectively

        Args:
            pin (int, optional): pin for the gripper PWM signal. Defaults to 16.
            open_angle (float, optional): Angle in degrees corresponding to open gripper. Defaults to 160.0.
            close_angle (float, optional): Angle in degrees corresponding to closed gripper. Defaults to 70.0.
        """
        self.servo: Servo = Servo(pin_id=pin)
        self.servo_top_angle: float = servo_top_angle
        self.servo_bottom_angle: float = servo_bottom_angle
        self.top_angle: float = 0.0
        self.bottom_angle: float = abs(self.servo_bottom_angle - self.servo_top_angle)
        self.sign: float = 1 if self.servo_bottom_angle > self.servo_top_angle else -1
        self.angle: float | None = None
        
    def lift(self, time:float = None) -> None:
        """Move gripper to the top
        """
        if time == None or self.angle == None:
            self.set_angle(self.top_angle)
        else:
            self.move(self.angle, self.top_angle, time)
        
        
    def lower(self, time: float = None) -> None:
        """Move gripper to the bottom
        """
        if time == None or self.angle == None:
            self.set_angle(self.bottom_angle)
        else:
            self.move(self.angle, self.bottom_angle, time)
            
    def move_by(self, d_angle: float) -> None:
        """Move the gripper by the angle increment given. Lower direction is +

        Args:
            d_angle (float): requested change in angle (degrees)
        """
        if self.angle == None: return
        
        new_angle = self.angle + d_angle
        if self.top_angle < new_angle < self.bottom_angle:
            self.set_angle(new_angle)

    def move_to(self, end_angle: float, time: float, num_angles:int = 100):
        """Move from the current angle to the end angle (in degrees) in the given amount of
        time (in seconds). 

        Args:
            end_angle (float): Ending angle of the motion, degrees
            time (float): time in which to make the motion, in seconds
            num_angles (int, optional): Number of steps to take. Defaults to 100.
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
        servo_angle: float = self.servo_top_angle + self.sign * angle
        self._set_servo_angle(servo_angle=servo_angle)
        self.angle = angle
        
    def _set_servo_angle(self, servo_angle: float) -> None:
        """Helper function to set servo angle based

        Args:
            servo_angle (float): servo angle in degrees
        """
        servo_angle: float = self._clamp(servo_angle, self.servo_bottom_angle, self.servo_top_angle)
        #servo_angle: float = min(self.servo_bottom_angle, max(self.servo_top_angle, servo_angle))
        print(f'Lifter servo angle = {servo_angle:.0f}')
        self.servo.write(servo_angle)
        #sleep(0.1)
        
    def _clamp(self, value: float, start: float, end: float) -> float:
        """Return value clamped between the other two values"""
        min_value = min(value, min(start, end))
        max_value = max(value, max(start, end))
        return min(max_value, max(min_value, value))
        
if __name__ == '__main__':
    lifter = Lifter()
    lifter.lift()
    sleep(0.5)
    lifter.lower()
    
    
#     for _ in range(5):
#         gripper.open()
#         sleep(1)
#         gripper.close()
#         sleep(1)
#     gripper.open()
#     sleep(2)

#     num_angles: int = 100
#     max_angle: float = 90.0
#     time: float = 3.0
#     d_angle: float = max_angle / (num_angles-1)
#     print(f'd_angle = {d_angle}')
#     d_time: float = time / (num_angles-1)
#     
#     for i in range(num_angles):
#         angle: float = i * d_angle
#         print(angle)
#         gripper.set_angle(angle)
#         sleep(d_time)
        
    


