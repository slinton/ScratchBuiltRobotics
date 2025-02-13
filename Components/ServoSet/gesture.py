#
# Gesture
#
# V2025_02_12_03
#
class Gesture:
    def __init__(self, times: list[float], indices: list[int], theta: list[list[float]]) -> None:
        self._times = times # normalized time points, [0, 1]
        self._indices = indices # indices of servos
        self._theta = theta # normalized angles for each servo at each time point, [0, 1]

    @property
    def indices(self) -> list[int]:
        return self._indices

    def get_thetas(self, time: float) -> list[float]:
        """Get the normalized angles for all servos at the given normalized time point.

        Args:
            time (float): normalized time point [0, 1]

        Raises:
            ValueError: if the time is out of range

        Returns:
            list[float]: normalized angles for all servos, [0, 1]
        """
        if time < self._times[0] or time > self._times[-1]:
            raise ValueError(f'Time {time} is out of range.')
        
        for i in range(len(self._times) - 1):
            if self._times[i] <= time and time <= self._times[i + 1]:
                xi: float = (t - self._times[i]) / (self._times[i + 1] - self._times[i])
                xim: float = 1.0 - xi
                return [xim * self._theta[j][i] + xi * self._theta[j][i+1] for j in range(len(self._indices))] 
            
    def check(self) -> None:
        # Check that the number of angles for each servo matches the number of time points
        for i in range(len(self._theta)):
            if len(self._theta[i]) != len(self._times):
                raise ValueError(f'Number of angles for servo {i} does not match number of time points.')
            
        # Check that the number of servo indices matches the number of servo angle lists
        if len(self._indices) != len(self._theta):
            raise ValueError('Number of servo angle lists does not match number of servo indices.')
        
        # Check that the servo indices are in range
        for i in range(len(self._indices)):
            if self._indices[i] < 0:
                raise ValueError(f'Servo index {self._indices[i]} is negative.')
            if self._indices[i] >= 16:
                raise ValueError(f'Servo index {self._indices[i]} is too large.')
            
            # Check that the theta values are in range
            for j in range(len(self._theta[i])):
                if self._theta[i][j] < 0.0 or self._theta[i][j] > 1.0:
                    raise ValueError(f'Angle {self._theta[i][j]} for servo {self._indices[i]} is out of range.')
    
    def __str__(self) -> str:
        return f'Gesture with {len(self._indices)} servos and {len(self._times)} time points.'


if __name__ == '__main__':
    gesture = Gesture(
        [0, 0.25, 0.5, 0.75, 1.0], [0, 1, 2], 
        [
            [0.0, 0.5, 1.0, 0.5, 0.0],
            [0.0, 0.5, 1.0, 0.5, 0.0],
            [0.0, 0.5, 1.0, 0.5, 0.0]
        ])
    
    print(gesture)
    gesture.check()

    num_steps: int = 10
    dt: float = 1.0 / num_steps
    
    for i in range(num_steps + 1):
        t: float = max(0, min(1.0, i * dt))
        print(f't: {t} {gesture.get_angles(t)}')
