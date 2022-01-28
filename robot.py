from sr.robot3 import *
R = Robot()
print("hello world")
import time 
POWER = 1
#R.power.beep(100, note="c")
#R.power.beep(100, note="c")
def move_forward():
    R.motor_board.motors[0].power = POWER
    time.sleep(10)
    
move_forward()
#R.power.beep(100, note="c")
move_forward()
#R.power.beep(100, note="d")
