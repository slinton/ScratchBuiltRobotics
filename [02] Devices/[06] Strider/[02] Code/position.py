#
# Position
# Static variable to keep track of the next id

# Version: 1.00
# Date: 2025-06-10
# Author: Sam Linton
# Description: A list of positions
#
class Position:
    _next_id = 0

    def __init__(self, angles: list[float], name: str = "") -> None:
        if name == "":
            name = f"Position {Position._next_id}"
            Position._next_id += 1
        self.name = name
        self._angles = angles

    # def clone(self, name: str = "") -> 'Position':
    #     return Position(self._angles.copy(), name)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def angles(self) -> list[float]:
        return self._angles


if __name__ == "__main__":
    # Test the Position class
    pos1 = Position([0.0, 0.0, 0.0], "Home")
    pos2 = Position([90.0, 45.0, 30.0])
    
    print(f"Position 1: {pos1.name}, Angles: {pos1.angles}")
    print(f"Position 2: {pos2.name}, Angles: {pos2.angles}")
    print(f"")
    
    pos2.name = "Custom Position"
    print(f"Updated Position 2: {pos2.name}, Angles: {pos2.angles}")