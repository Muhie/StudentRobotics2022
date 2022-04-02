from sr.robot3 import *
import time

R = Robot()
print("starting")
# motor board srABC1, channel 0 to full power forward
R.motor_boards['SR0WE7'].motors[0].power = 0.1
print("mb1 m1 on")
R.motor_boards['SR0WE7'].motors[1].power = 0.1
print("mb1 m2 on")
# motor board srXYZ1, channel 0 to full power reverse
R.motor_boards['SR0JH18'].motors[0].power = 0.1
print("mb2 m1 on")
R.motor_boards['SR0JH18'].motors[1].power = 0.1
print("mb2 m2 on")
time.sleep(2)
print("finished")
# motor board srABC1, channel 1 to half power forward
#R.motor_boards["srABC1"].motors[1].power = 0.5