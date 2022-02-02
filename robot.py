from sr.robot3 import *
print("hello world")
import time 



class Movement():
    def __init__(self, R, motorboard1, motorboard2):
        self.R = R
        self.fb = motorboard1
        self.bb = motorboard2
        self.fb_l_power = 0
        self.fb_r_power = 0
        self.bb_l_power = 0
        self.bb_r_power = 0
        self.master_power = 0.1
    
    def move(self):
        self.R.motor_boards[self.fb].motors[0].power = self.fb_l_power
        self.R.motor_boards[self.fb].motors[1].power = self.fb_r_power
        self.R.motor_boards[self.bb].motors[0].power = self.bb_l_power
        self.R.motor_boards[self.bb].motors[1].power = self.bb_r_power
    
    def forwards(self):
        self.fb_l_power = self.master_power
        self.fb_r_power = self.master_power
        self.bb_r_power = self.master_power
        self.bb_l_power = self.master_power
        self.move()

    def backwards(self):
        self.fb_l_power = -self.master_power
        self.fb_r_power = -self.master_power
        self.bb_r_power = -self.master_power
        self.bb_l_power = -self.master_power
        self.move()

    def left(self):
        self.fb_l_power = self.master_power
        self.fb_r_power = -self.master_power
        self.bb_r_power = -self.master_power
        self.bb_l_power = self.master_power
        self.move()

    def right(self):
        self.fb_l_power = -self.master_power
        self.fb_r_power = self.master_power
        self.bb_r_power = self.master_power
        self.bb_l_power = -self.master_power
        self.move()

    def start(self):
        self.forwards()
        time.sleep(5)
        self.backwards()
        time.sleep(5)
        self.left()
        time.sleep(5)
        self.right()
        time.sleep(5)



def main():
    R = Robot()
    motorboard1 = 'SR0WE7' #Front motorboard
    motorboard2 = 'SR0JH18' #Back motorboard
    robo = Movement(R, motorboard1, motorboard2)
    robo.start()



if __name__ == '__main__':
    main()