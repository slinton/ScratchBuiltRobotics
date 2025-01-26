#
# ServoInfo
#
class ServoInfo:
    def __init__(self, 
                 name: str,
                 index: int,
                 angle_start: float, 
                 angle_end: float
                 ) -> None:
        self.name = name
        self.index = index
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.sign = 1 if angle_end > angle_start else -1

    @property
    def name(self) -> str:
        return self._name
    
    def _angle_in_range(self, angle: float) -> bool:
        return  (self.angle_end - angle) * (angle - self.angle_start) >= 0
   