#
# InertialSensor
# 2024_12_30
#
from imu import MPU6050
from time import sleep, ticks_us

class InertialSensor(MPU6050):
    """Wrapper class for MPU6050 imu that measures heading based on its
    inital value and gyro readings
    """
    
    def __init__(self, i2c, heading_threshold: float=0.0)-> None:
        super().__init__(i2c)
        self._heading: float = 0.0
        self._heading_drift: float = 0.0 # Rate of drift, deg per sec
        self._winding: int = 0 # For conversion back to total rotation
        self._heading_threshold = heading_threshold # Ignore values less than this
        self._update_ticks_us = ticks_us()
        
    @property
    def heading(self)-> float:
        return self._heading
    
    @property
    def raw_heading(self)-> float:
        return 360.0 * self._winding + self._heading
    
    def calibrate(self)-> None:
        self.calibrate_heading(heading=0.0)
        
    def calibrate_heading(self, heading: float=0.0)-> None:
        """Measure the drift of the sensor when not in motion so it
        can be compensated for
        """
        # TODO Fix this
        print('Calibrating...', end='')
        num_samples: int = 100
        sample_time: float = 0.01
        
        heading_start: float = self._heading
        time_start: float = self._update_ticks_us
        for i in range(num_samples):
            self.update()
            sleep(sample_time)
        heading_end: float = self._heading
        time_end: float = self._update_ticks_us
            
        self._heading = heading
        self._heading_drift = 1.0e06 * (heading_end - heading_start) / (time_end - time_start)
        print(f'complete. Heading drift = {self._heading_drift}')
            
    def update(self)-> None:
        self.update_heading()
        self._update_ticks_us = ticks_us()
        
    def update_heading(self)-> None:
        """Update the value of the heading based on the gyro z value
        """
        # TODO: make this real
        gyro_z: float = self.gyro.z - self._heading_drift
        gyro_z = gyro_z if abs(gyro_z) >= self._heading_threshold else 0.0
        dt: float = max(0.0, 1.0e-06 * (ticks_us() - self._update_ticks_us))
        self._heading += dt * gyro_z
        self._heading, self._winding = self._transform_angle(self._heading, self._winding)
        
    def _transform_angle(self, angle: float, winding: int)-> float:
        while angle >= 360.0:
            angle -= 360.0
            winding += 1
        while angle < 0.0:
            angle += 360.0
            winding -= 1
        return angle, winding

    