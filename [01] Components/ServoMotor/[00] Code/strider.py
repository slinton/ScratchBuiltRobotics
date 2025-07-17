#
# Strider
#
# Version: 1.00
# Date: 2025-07-15
# Author: Sam Linton
# Description: Legged robot
#
from servo_set_reader import ServoSetReader
from servo_set import ServoSet
from position_reader import PositionReader
from position import Position
from movement import Movement


class Strider:
    def __init__(self):
       self._front_left_leg: ServoSet = ServoSetReader.create_servo_from_file(f"front_left_leg.srv")
       self._front_right_leg: ServoSet = ServoSetReader.create_servo_from_file(f"front_right_leg.srv")
       self._back_left_leg: ServoSet = ServoSetReader.create_servo_from_file(f"rear_left_leg.srv")
       self._back_right_leg: ServoSet = ServoSetReader.create_servo_from_file(f"rear_right_leg.srv")

       self._positions: list[Position] = PositionReader.read_positions_from_file("strider.pos")

       self.home()

    def home(self) -> None:
        """Home all legs."""
        for leg in [self._front_left_leg, self._front_right_leg, self._back_left_leg, self._back_right_leg]:
            leg.move_to_position(leg.get_home_position())

    def move_to_position(self, position_name: str, time: float = 0.0, num_steps: int = 10) -> None:
        """Move to a named position."""
        position: Position = next(pos for pos in self._positions if pos.name == position_name)

        
        for leg in [self._front_left_leg, self._front_right_leg, self._back_left_leg, self._back_right_leg]:
            leg.move_to_position(position, time, num_steps) 

    


if __name__ == '__main__':
    strider = Strider()
    strider.move_to_position("forward", time=1.0, num_steps=20)
    strider.move_to_position("home", time=1.0, num_steps=20)
    