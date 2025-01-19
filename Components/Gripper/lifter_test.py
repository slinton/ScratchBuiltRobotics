from servo import Servo
from time import sleep
  
ang_g0 = 75
ang_g1 = 100
dang_g = ang_g1 - ang_g0
gripper = Servo(pin_id=17)
gripper.write(ang_g0)

ang_l0 = 0
ang_l1 = 180
dang_l = ang_l1 - ang_l0
lifter = Servo(pin_id=16)
lifter.write(ang_l0)


num_steps = 100
t_final = 0.25
dt = t_final / (num_steps-1)

for n in range(num_steps):
    xi = n / (num_steps-1)
    ang_g = ang_g0 + xi*dang_g
    ang_l = ang_l0 + xi*dang_l
    print(f'{ang_l} {ang_g}')
    gripper.write(ang_g)
    lifter.write(ang_l)
    sleep(dt)
    
for n in range(num_steps):
    xi = n / (num_steps-1)
    ang_g = ang_g1 - xi*dang_g
    ang_l = ang_l1 - xi*dang_l
    print(f'{ang_l} {ang_g}')
    gripper.write(ang_g)
    lifter.write(ang_l)
    sleep(dt)