from sr.robot3 import *
print("hello world")
import time



class Collybot(Robot):
    def __init__(self):
        super().__init__() #call ronot contructor
        self.fb = 'SR0WE7' #Front motorboard
        self.bb = 'SR0JH18' #Back motorboard
        
        self.marker_ids = self.camera.save(self.usbkey / "initial-view.png")
        
        self.fb_0_power = 0
        self.fb_1_power = 0
        self.bb_0_power = 0
        self.bb_1_power = 0
        self.master_power = 0.15
    
    def move(self):
        self.fb.motors[0].power = self.fb_0_power
        self.fb.motors[1].power = self.fb_1_power
        self.bb.motors[0].power = self.bb_0_power
        self.bb.motors[1].power = self.bb_1_power
    
    def forwards(self):
        self.fb_0_power = self.master_power
        self.fb_1_power = self.master_power
        self.bb_0_power = self.master_power
        self.bb_1_power = self.master_power
        self.move()

    def backwards(self):
        self.fb_0_power = -self.master_power
        self.fb_1_power = -self.master_power
        self.bb_0_power = -self.master_power
        self.bb_1_power = -self.master_power
        self.move()

    def left(self):
        self.fb_0_power = 2*self.master_power
        self.fb_1_power = -2*self.master_power
        self.bb_0_power = -2*self.master_power
        self.bb_1_power = 2*self.master_power
        self.move()

    def right(self):
        self.fb_0_power = -2*self.master_power
        self.fb_1_power = 2*self.master_power
        self.bb_0_power = 2*self.master_power
        self.bb_1_power = -2*self.master_power
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


        marker_ids = self.camera.save(self.usbkey / "initial-view.png")

        while True:
            markers = self.camera.see()
            print("I can see", len(markers), "markers:")

            for m in markers:
                print(" - Marker #{0} is {1} metres away".format(m.id, m.distance))



def main():
    jeff = Collybot()
    
    
    jeff.start()
    




if __name__ == '__main__':
    main()

