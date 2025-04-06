#
# drive_train_test
#
# Version 25_04_01_01
#
from drive_train import DriveTrain
from time import sleep

        
# Test the DriveTrain class
if __name__ == "__main__":
    print('Testing DriveTrain class')
    # Create the DriveTrain object
    #dt = DriveTrain((1, 2), (3, 4))
    dt = DriveTrain()
    print(repr(dt))
    
    # Test the forward method
    print("Testing forward method")
    dt.forward(100)
    dt.print_state()
    sleep(2)
    
    # Test the backward method
    print("Testing backward method")
    dt.backward(100)
    dt.print_state()
    sleep(2)
    
    # Test the turn_left method
    print("Testing turn_left method")
    dt.turn_left(100)
    dt.print_state()
    sleep(2)
    
    # Test the turn_right method
    print("Testing turn_right method")
    dt.turn_right(100)
    dt.print_state()
    sleep(2)
    
    # Test the stop method
    print("Testing stop method")
    dt.stop()
    dt.print_state()
    sleep(2)
    
    # Test the move method
    print("Testing move method")
    dt.move(100, 100)
    dt.print_state()
    sleep(2)
    
    print("Testing stop method")
    dt.stop()
    dt.print_state()
    sleep(2)
    
    print("Test swerve left")
    dt.move(75, 100)
    dt.print_state()
    sleep(2)
    
    print("Test swerve right")
    dt.move(100, 75)
    dt.print_state()
    sleep(2)
    
    dt.stop()
    
    print("Test complete")
