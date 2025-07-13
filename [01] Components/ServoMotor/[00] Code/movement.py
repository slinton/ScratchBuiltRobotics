#
# Movement
#
# Version: 1.00
# Date: 2025-07-10
# Author: Sam Linton
# Description: A list of sequential positions
#
from position import Position

class Movement:
    def __init__(self, positions: list[Position], times: list[float] = []) -> None:
        self._positions: list[Position] = positions
        if len(times) == 0:
            self._times = [i for i in range(len(positions))]
        elif len(times) != len(positions):
            raise ValueError("Times list must be same length as positions list")
        else:        self._times: list[float] = times

    def __getitem__(self, index: int) -> tuple[float, Position]:
        return self._times[index], self._positions[index]

    def __len__(self) -> int:
        return len(self._positions)
    
    @property
    def num_positions(self) -> int:
        return len(self._positions)
        
    
        