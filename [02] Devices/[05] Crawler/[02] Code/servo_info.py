#
# ServoInfo
#
# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
# Description: Encapsulation of servo information for controlling servos in a robotic application.
#
# TODO: perhaps add a "home" value; maybe create a Joint subclass.
#
class ServoInfo:
    """Encapsulation of servo information.
    Note that "angle" represents the logical angle as determined by the application, wherease "servo_angle"
    represents the physical angle of the servo. servo_angle_0 is the angle of the servo when the logical
    angle is 0.
    The logical angle is constrained between angle_start and angle_end. This is usually to keep the servo 
    within its physical limits, but it can also be used to limit the range of motion for a specific application.
    All angles are in degrees.
    
    So:
        servo_angle = servo_angle_0 + sign * angle
        angle = sign * (servo_angle - servo_angle_0)

    where sign is either +1 or -1.
    The sign is used to determine whether the servo angle increases with increasing logical angle.

    """
    def __init__(self, 
                 index: int = 0,
                 servo_angle_0: float = 0.0, # Servo angle corresponding to angle = 0.0
                 sign: int = 1, # Positive if the servo angle increases with increasing logical angle
                 angle_start: float = 0.0, # Logical starting angle
                 angle_end: float = 180.0, # Logical ending value
                 name: str | None = None, # name: str | None = None
                 ) -> None:
        """Constructor for ServoInfo.

        Args:
            index (int, optional): Used as an index into an external array of ServoInfo. Defaults to 0.
            servo_angle_0 (float, optional): physical angle of the servo when the logical angle is 0. Defaults to 0.0.
            sign (int, optional): +1 if the servo angle increases with increasing logical angle, -1 if it decreases. Defaults to 1.
            angle_start (float, optional): logical starting angle in degrees. Defaults to 0.0.
            angle_end (float, optional): logical ending angle in degrees. Defaults to 180.0.
            name (str | None, optional): Name of the servo. Defaults to None, which will set it to 'Servo: {index}'.
        """
        self._index: int = index # For use with servo sets
        self._servo_angle_0: float = servo_angle_0
        self._sign: int = sign
        self._angle_start: float = angle_start
        self._angle_end: float = angle_end
        self._name: str = f'Servo: {str(index)}' if name is None or name == '' else name
        self._angle: float | None = None

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def index(self) -> int:
        return self._index
    
    @property
    def angle(self) -> float:
        if self._angle is None:
            raise ValueError('Angle has not been set!')
        return self._angle
    
    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value
    
    def angle_in_range(self, angle: float) -> bool:
        """Return True if the logical angle is within the specified range.

        Args:
            angle (float): angle in degrees to check

        Returns:
            bool: true if the angle is within the specified range of motion
        """
        return  (self._angle_end - angle) * (angle - self._angle_start) >= 0.0
    
    def get_servo_angle(self, angle: float) -> float:
        """Get the servo angle from the logical angle.

        Args:
            angle (float): logical angle in degrees

        Returns:
            float: servo angle in degrees
        """
        return self._servo_angle_0 + self._sign * angle
    
    def get_angle(self, servo_angle: float) -> float:
        """Get the logical angle from the servo angle.

        Args:
            servo_angle (float): servo angle in degrees

        Returns:
            float: logical angle in degrees
        """
        return self._sign * (servo_angle - self._servo_angle_0)
    
    def __str__(self) -> str:
        return f'Servo Info {self._name} at index {self._index}. Angle: {self._angle} Range: {self._angle_start}-{self._angle_end} 0 angle = {self._servo_angle_0}'
    
   
if __name__ == "__main__":
    # Test code
    servo_info = ServoInfo(index=2, servo_angle_0=90, sign=-1, angle_start=0, angle_end=180, name='Servo 2')
    print(servo_info)

