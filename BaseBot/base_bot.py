 #
 # BaseBot
 #
from drive_train import DriveTrain
 
class BaseBot:
    """Class representing a robot with a drive train.
    """
    def __init__(self, drive_train: DriveTrain)-> None:
        """Initialize the BaseBot object with a drive train."""
        
        self._drive_train = drive_train

    def move(self, left_speed: int, right_speed: int)-> None:
        """Arbitrary motion, controlling the speed of each motor independently

        Args:
            left_speed (int): speed of left motor, (-100 , +100)
            right_speed (int): speed of right motor, (-100 , +100)
        """
        
        self._drive_train.move(left_speed, right_speed)
        
    def forward(self, speed: int)-> None:
        """Drive the robot forward at a given speed.

        Args:
            speed (int): speed of the robot in the range (-100, +100)
        """
        
        self._drive_train.forward(speed)
        
    def backward(self, speed: int)-> None:
        """Drive the robot backward at a given speed. Note that the same
        effect can be achieved by calling forward with a negative speed.

        Args:
            speed (int): backwards speed of the robot in the range (0-100)
        """
        
        self._drive_train.backward(speed)    
        
    def turn_left(self, speed: int)-> None:
        """Turn the robot left at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
        """
        
        self._drive_train.turn_left(speed)  
        
    def turn_right(self, speed: int)-> None:
        """Turn the robot right at a given speed.

        Args:
            speed (int): speed of the robot in the range 0-100
        """
        
        self._drive_train.turn_right(speed) 
        
    def stop(self)-> None:
        """Stop the robot."""
        
        self._drive_train.stop()