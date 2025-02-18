#
# Gesture
#
# V2025_02_17_02
#

class Gesture:
    """Encapsulates a sequence of angles over (normalized) time for a set of servos.
    The angles are the logical values for the servos in degrees
    """
    def __init__(self, times: list[float], indices: list[int], angles: list[list[float]], name: str = '') -> None:
        self._times: list[float] = times # normalized time points, [0, 1]
        self._indices: list[int] = indices # indices of servos
        self._angles: list[list[float]] = angles # angles for each servo at each time point, degrees
        self._name: str = name

    @property
    def indices(self) -> list[int]:
        return self._indices

    def get_angles(self, time: float) -> list[float]:
        """Get the angles in degrees for all servos at the given normalized time point.

        Args:
            time (float): normalized time point [0, 1]

        Raises:
            ValueError: if the time is out of range

        Returns:
            list[float]: normalized angles for all servos, degrees
        """
        if time < self._times[0] or time > self._times[-1]:
            raise ValueError(f'Time {time} is out of range.')
        
        for i in range(len(self._times) - 1):
            if self._times[i] <= time and time <= self._times[i + 1]:
                xi: float = (time - self._times[i]) / (self._times[i + 1] - self._times[i])
                xim: float = 1.0 - xi
                return [xim * self._angles[j][i] + xi * self._angles[j][i+1] for j in range(len(self._indices))] 
            
    def check(self) -> None:
        """Check that the gesture is valid.
        """
        # Check that the number of angles for each servo matches the number of time points
        for i in range(len(self._angles)):
            if len(self._angles[i]) != len(self._times):
                raise ValueError(f'Number of angles for servo {i} does not match number of time points.')
            
        # Check that the number of servo indices matches the number of servo angle lists
        if len(self._indices) != len(self._angles):
            raise ValueError('Number of servo angle lists does not match number of servo indices.')
        
        # Check that the servo indices are in range
        for i in range(len(self._indices)):
            if self._indices[i] < 0:
                raise ValueError(f'Servo index {self._indices[i]} is negative.')
            if self._indices[i] >= 16:
                raise ValueError(f'Servo index {self._indices[i]} is too large.')
    
    def __str__(self) -> str:
        return f'Gesture {self._name} with {len(self._indices)} servos and {len(self._times)} time points.'
    
    def print_all_values(self) -> None:
        """Print all values for the gesture.
        """
        print(self)
        print('Servo indices:', gesture.indices)
        for i in range(len(self._times)):
            print(f'Time {self._times[i]:.2f}', end=': ')
            for j in range(len(self._indices)):
                print(f'{self._angles[j][i]:3.0f}', end='\t ')
            print()

    def __add__(self, other: 'Gesture') -> 'Gesture':
        """Add two gestures together, one after the other
        """
        num_servos: int = len(self._indices)

        # Check that the indices match
        if num_servos != len(other._indices):
            raise ValueError('Number of servos does not match.')
        for i in range(num_servos):
            if self._indices[i] != other._indices[i]:
                raise ValueError('Servo indices do not match.')
            
        # Create new times values. # TODO: what about time = 0.5
        new_times: list[float] = [0.5*time for time in self._times]
        new_times += [0.5 + 0.5*time for time in other._times]

        # Combine angle values
        new_angles: list[list[float]] = [[] for _ in range(num_servos)]
        for i in range(num_servos):
            new_angles[i] = self._angles[i] + other._angles[i]
        
        return Gesture(new_times, self._indices, new_angles, f'{self._name} + {other._name}') 
    
if __name__ == '__main__':
    # Test code
    from time import sleep
    
    gesture = Gesture(
        [0, 0.25, 0.5, 0.75, 1.0],
        [0, 1, 2], 
        [
            [0.0, 40.0, 90.0, 40.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0]
        ], 'Generic')
    
    print(gesture)
    gesture.check()

    gesture.print_all_values()

    num_steps: int = 10
    dt: float = 1.0 / num_steps
    
    print('Servo indices:', gesture.indices)
    for i in range(num_steps + 1):
        t: float = max(0, min(1.0, i * dt))
        angle: list[float] = gesture.get_angles(t)
        print(f't: {t:3.1f}', end='\t')
        for j in range(len(gesture.indices)):
            print(f' {gesture.get_angles(t)[j]:3.0f}', end='\t')
        print()
