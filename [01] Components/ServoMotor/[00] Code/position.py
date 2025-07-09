#
# Position
#
# Version: 1.00
# Date: 2025-07-07
# Author: Sam Linton
# Description: A list of angles for a set of servos
#
class Position:
    def __init__(self, angles: list[float], name: str = "") -> None:
        self._name = name
        self._angles = angles
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def angles(self) -> list[float]:
        return self._angles
    
    @property
    def num_angles(self) -> int:
        return len(self._angles)
    
    def __getitem__(self, index: int) -> float:
        return self._angles[index]


if __name__ == "__main__":
    # Test the Position class
    pos1 = Position([30.0, 40.0, 50.0], "Home")
    pos2 = Position([90.0, 45.0, 30.0], "Custom Position")


    
    print(f"Position 1: {pos1.name}, Angles: {pos1.angles}")
    print(f"Position 2: {pos2.name}, Angles: {pos2.angles}")
    print(f"")
    for _ in range(pos1.num_angles):
        print(f"Position 1 Angle {_}: {pos1[_]}")
    
