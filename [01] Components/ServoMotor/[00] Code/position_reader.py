#
# PositionReader
#
# Version: 1.00
# Date: 2025-07-15
# Author: Sam Linton
# Description: Reads position data from a file
from position import Position

class PositionReader:
   
    @classmethod
    def read_positions_from_file(cls, filename: str) -> list[Position]:
        positions: list[Position] = []

        with open(filename, 'r') as f:
            line: str = f.readline().strip()
            while line != '':
                if not line.startswith('#'):
                    words = line.split(',')
                    name: str = words[0].strip()
                    angles: list[float] = [float(angle.strip()) for angle in words[1:]]
                    position = Position(angles=angles, name=name)
                    positions.append(position)
                line = f.readline().strip()

        return positions

   


if __name__ == '__main__':
    #import os
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "strider.pos"
    #full_path = os.path.join(script_dir, filename)
    full_path = filename  # Assuming the file is in the same directory as this script
    print(full_path)
    positions: list[Position] = PositionReader.read_positions_from_file(full_path)
    for position in positions:
        print(f"Position: {position.name}, Angles: {position.angles}")
