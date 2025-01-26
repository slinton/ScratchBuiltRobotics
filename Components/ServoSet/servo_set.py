#
# ServoSet
#
class ServoSet:
    """Uses the PCA9685 to control a set of servos.
    """

    def __init__(self, i2c) -> None:
        """_summary_

        Args:
            i2c (_type_, optional): _description_. Defaults to i2c.

        Returns:
            _type_: _description_
        """
        self._i2c = i2c


    def write(self, index, degrees) -> None:
        pass
        # span = self.max_duty - self.min_duty
        # if degrees is not None:
        #     duty = self.min_duty + span * degrees / self.degrees
        # elif radians is not None:
        #     duty = self.min_duty + span * radians / math.radians(self.degrees)
        # elif us is not None:
        #     duty = self._us2duty(us)
        # elif duty is not None:
        #     pass
        # else:
        #     return self.pca9685.duty(index)
        # duty = min(self.max_duty, max(self.min_duty, int(duty)))
        # self.pca9685.duty(index, duty)

    def read(self, index) -> float:
        pass
        

    # TODO: Add asynchronous

