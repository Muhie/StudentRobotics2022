from sr.robot3 import *
print("hello world")
import time



class Collybot(Robot):
    def __init__(self):
        super().__init__() #call robot contructor
        self.fb = self.motor_boards['SR0WE7'] #Front motorboard
        self.bb = self.motor_boards['SR0JH18'] #Back motorboard
        #self.servo=self.servo_board.servos[0]
        self.marker_ids = self.camera.save(self.usbkey / "initial-view.png")
        self.fov = 60
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.master_power = 0.2

    def power_H0(self):
        self.power_board.outputs[OUT_H0].is_enabled = True

    def depower_H0(self):
        self.power_board.outputs[OUT_H0].is_enabled = False

    def power_H1(self):
        self.power_board.outputs[OUT_H1].is_enabled = True

    def depower_H1(self):
        self.power_board.outputs[OUT_H1].is_enabled = False

    def power_L0(self):
        self.power_board.outputs[OUT_L0].is_enabled = True

    def depower_L0(self):
        self.power_board.outputs[OUT_L0].is_enabled = False

    def power_L1(self):
        self.power_board.outputs[OUT_L1].is_enabled = True

    def depower_L1(self):
        self.power_board.outputs[OUT_L1].is_enabled = False

    def power_L2(self):
        self.power_board.outputs[OUT_L2].is_enabled = True

    def depower_L2(self):
        self.power_board.outputs[OUT_L2].is_enabled = False

    def power_L3(self):
        self.power_board.outputs[OUT_L3].is_enabled = True

    def depower_L3(self):
        self.power_board.outputs[OUT_L3].is_enabled = False
    
    def apply(self):
        self.fb.motors[0].power=self.fl
        self.fb.motors[1].power=self.fr
        self.bb.motors[0].power=self.bl
        self.bb.motors[1].power=self.br

    def forwards(self):
        print("moving forwards")
        self.fl = self.master_power
        self.fr = self.master_power
        self.bl = self.master_power
        self.br = self.master_power
        self.apply()

    def backwards(self):
        print("moving backwards")
        self.fl = -self.master_power
        self.fr = -self.master_power
        self.bl = -self.master_power
        self.br = -self.master_power
        self.apply()

    def left(self):
        print("moving left")
        self.fl = 2*self.master_power
        self.fr = -2*self.master_power
        self.bl = -2*self.master_power
        self.br = 2*self.master_power
        self.apply()

    def right(self):
        print("moving right")
        self.fl = -2*self.master_power
        self.fr = 2*self.master_power
        self.bl = 2*self.master_power
        self.br = -2*self.master_power
        self.apply()

    def stop(self):
        print("stopping")
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.apply()

    def movement_test(self):
        print("starting movement test")
        self.left()
        time.sleep(5)
        self.right()
        time.sleep(5)
        self.forwards()
        time.sleep(5)
        self.backwards()
        time.sleep(5)
        self.stop()


    def marker(self):
        self.markers = self.camera.see()

    def marker_ids(self):
        self.markers = self.camera.see_ids()
    
    def marker_test(self):
        print("starting marker test")
        while True:
            markers = self.camera.see()
            print("I can see", len(markers), "markers:")
            if markers:
                self.forwards()
            for m in markers:
                print(" - Marker #{0} is {1} metres away".format(m.id, m.distance))

    def emergancy(self):
        #Emergancy shutdown, logs power status of battery
        self.power_board.outputs.power_off()
        print(self.power_board.battery_sensor.current)
        print(self.power_board.battery_sensor.voltage)

    def locator(self):
        self.marker_ids()
        if len(self.markers) > 0:
            self.marker()
            if len(self.markers) > 0:
                print('To locate')

    def start(self):
        self.power_H1()
        self.power_H0()
        self.movement_test()
        #self.servo_test()
        #self.marker_test()
    
    def servo_test(self):
        self.servo.position=0.5
        time.sleep(5)
        self.servo.position=-0.5
        time.sleep(5)
        self.servo.position=None

def main():
    jeff = Collybot()
    jeff.start()
    


if __name__ == '__main__':
    main()

