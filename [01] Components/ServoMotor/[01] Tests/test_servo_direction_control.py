import uasyncio as asyncio
from pwm_servo_motor import PWMServoMotor


async def control_func(servo):
    for _ in range(5):
        servo.start_increasing()
        await asyncio.sleep_ms(500)
        servo.stop()
        await asyncio.sleep_ms(500)
        servo.start_decreasing()
        await asyncio.sleep_ms(500)
        servo.stop()
        
    
    

if __name__ == '__main__':
    servo = PWMServoMotor(pin = 16)
    servo.set_angle(0)
    asyncio.run( asyncio.gather(servo.run_loop(), control_func(servo)))
    
    
    