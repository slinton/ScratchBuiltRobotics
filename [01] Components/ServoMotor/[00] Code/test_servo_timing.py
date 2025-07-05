#
# test_servo_timing
#
from PWM_servo_motor import PWMServoMotor
from time import sleep, ticks_us

servo = PWMServoMotor(pin = 16)

start_angle = 0
end_angle = 90


servo.write_angle(start_angle)
sleep(0.5)

start_ticks = ticks_us()
servo.write_angle(end_angle)
end_ticks = ticks_us()

elapsed_ticks = end_ticks - start_ticks
elapsed_seconds = elapsed_ticks / 1_000_000 
rate = (end_angle - start_angle) / elapsed_seconds
print(f"Elapsed time: {elapsed_seconds:.6f} seconds")
print(f"Rate of change: {rate:.2f} degrees/second")
