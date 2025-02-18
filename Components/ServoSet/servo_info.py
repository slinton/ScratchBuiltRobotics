#
# ServoInfo
#
# V2025_02_17_01
# TODO: maybe add in named values? e.g., 'home', 'flexed', 'extended', etc.
#
class ServoInfo:
    """Encapsulation of servo information.
    Note that angle represents the logical angle as determined by the application, wherease servo_angle
    represents the physical angle of the servo. servo_angle_0 is the angle of the servo when the logical
    angle is 0.0.
    So servo_angle = servo_angle_0 + sign * angle
    The logical angle is constrained between angle_start and angle_end.
    """
    def __init__(self, 
                 index: int = 0,
                 servo_angle_0: float = 0.0, # Servo angle corresponding to angle = 0.0
                 sign: int = 1, # Positive if the servo angle increases with increasing logical angle
                 angle_start: float = 0.0, # Logical starting angle
                 angle_end: float = 180.0, # Logical ending value
                 name: str | None = None, # name: str | None = None
                 ) -> None:
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
        return f'Servo Info {self._name} at index {self._index}. Angle: {self._angle} Range: {self._angle_start}-{self._angle_end}'
    
   
if __name__ == "__main__":
    # Test code
    servo_info = ServoInfo(index=2, servo_angle_0=90, sign=-1, angle_start=0, angle_end=180, name='Servo 2')
    print(servo_info)

