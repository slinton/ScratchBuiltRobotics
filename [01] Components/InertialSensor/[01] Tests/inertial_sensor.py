#
# InertialSensor
# V2025_02_11_02
#
# TODO: x-value drifts like crazy
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
        
        self._x: float = 0.0 # cm
        self._v: float = 0.0 # cm /s
        self._a: float = 0.0 # cm /s^2
        self._a_drift: float = 0.0 # cm / s^2
        self._a_threshold = 0.07 # cm / s^2

        self._update_ticks_us = ticks_us()
        
    @property
    def x(self)-> float:
        return self._x
    
    @x.setter
    def x(self, value) -> None:
        self._x = value
    
    @property
    def v(self)-> float:
        return self._v
    
    @v.setter
    def v(self, value) -> None:
        self._v = value
    
    @property
    def a(self)-> float:
        return self._a
        
    @property
    def heading(self)-> float:
        return self._heading
    
    @property
    def raw_heading(self)-> float:
        return 360.0 * self._winding + self._heading
    
    def calibrate(self)-> None:
        self.calibrate_heading(heading=0.0)
        self.calibrate_accel()
        
    def calibrate_heading(self, heading: float=0.0)-> None:
        """Measure the drift of the sensor when not in motion so it
        can be compensated for
        """
        # TODO: probably don't use update here

        print('Calibrating Heading...', end='')
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
        
    def calibrate_accel(self) -> None:
        """Measure the zero-motion x-acceleration value
        """
        print('Calibrating acceleration...', end='')
        num_samples: int = 100
        sample_time: float = 0.01
        a_min: float = 1.0
        a_max: float = -1.0
        
        accel: float = 0.0 # in g's
        for _ in range(num_samples):
            a = self.accel.x
            a_min = min(a, a_min)
            a_max = max(a, a_max)
            accel += self.accel.y
            sleep(sample_time)
            
        self._a_drift = 9.81 * accel / num_samples # in cm/s^2
        self._x = 0.0
        self._v = 0.0
        self._a = 0.0
        print(f'complete. Acceleration drift = {self._a_drift} cm/s^2 {a_min=} {a_max=}')
            
    def update(self)-> None:
        self.update_heading()
        self.update_x()
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

    def update_x(self)-> None:
        """Update the value of x based on the accelerometer x value
        """
        dt: float = max(0.0, 1.0e-06 * (ticks_us() - self._update_ticks_us))
        a_new = self.accel.y * 9.81 - self._a_drift  # cm/s^2
        a_new = a_new if abs(a_new) > self._a_threshold else 0.0
        
        a_old: float = self._a
        v_old: float = self._v
        
        self._a = a_new  # cm/s^2
        self._v += 0.5 * (a_old + a_new) * dt # cm/s
        self._x += 0.5 * (v_old + self._v) * dt # cm
        
    def _transform_angle(self, angle: float, winding: int)-> float:
        while angle >= 360.0:
            angle -= 360.0
            winding += 1
        while angle < 0.0:
            angle += 360.0
            winding -= 1
        return angle, winding
