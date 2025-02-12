#
# ServoInfo
#
# V2025_02_11_01
#
class ServoInfo:
    def __init__(self, 
                 index: int,
                 angle_start: float = 0.0, 
                 angle_end: float = 180.0,
                 name = None, # name: str | None = None
                 ) -> None:
        self._name: str = f'Servo: {str(index)}' if name is None or name == '' else name
        self._index: int = index # For use with servo sets
        self._angle_start: float = angle_start
        self._angle_end: float = angle_end
        self._angle: float | None = None
        self._sign: int = 1 if angle_end > angle_start else -1

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def angle(self) -> float:
        if self._angle is None:
            raise ValueError('Angle has not been set!')
        return self._angle
    
    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value;
    
    def angle_in_range(self, angle: float) -> bool:
        return  (self._angle_end - angle) * (angle - self._angle_start) >= 0.0
    
    def __str__(self) -> str:
        return f'Servo Info {self._name} at index {self._index}. Angles {self._angle_start}-{self._angle_end}'
    
   
