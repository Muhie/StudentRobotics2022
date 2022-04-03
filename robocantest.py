import cv2
import numpy as np
from sr.robot3 import *
print("hello world")
import time



class Collybot(Robot):
    def __init__(self):
        super().__init__() #call robot contructor
        self.fb = self.motor_boards['SR0WE7'] #Front motorboard
        self.bb = self.motor_boards['SR0JH18'] #Back motorboard
        # self.servo=self.servo_board.servos[0]
        self.marker_ids = self.camera.save(self.usbkey / "initial-view.png")
        self.fov = 60
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.motor_sf = 2
        self.master_power = 0
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3,640)
        self.cap.set(4,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 10)
        self.classNames = []
        classFile = "coco.names"
        with open(classFile,"rt") as f:
            self.classNames = f.read().rstrip("\n").split("\n")
        self.configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        self.weightsPath = "frozen_inference_graph.pb"
        self.net = cv2.dnn_DetectionModel(self.weightsPath,self.configPath)
        self.net.setInputSize(200,200)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)

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
    
    def slow(self):
        self.master_power = 0.15
        print('Change to slow speed')
        self.scale_conversion()

    def medium(self):
        self.master_power = 0.3
        print('Change to medium speed')
        self.scale_conversion()

    def fast(self):
        self.master_power = 0.5
        print('Change to fast speed')
        self.scale_conversion()

    def scale_conversion(self):
        self.front_master_power = self.master_power/self.motor_sf
        self.back_master_power = self.master_power

    def move(self):
        self.fb.motors[1].power=self.fl
        self.fb.motors[0].power=self.fr
        self.bb.motors[0].power=self.bl
        self.bb.motors[1].power=self.br

    def forwards(self):
        print("moving forwards")
        self.fl = self.front_master_power
        self.fr = self.front_master_power
        self.bl = self.back_master_power
        self.br = self.back_master_power
        self.move()

    def backwards(self):
        print("moving backwards")
        self.fl = -self.front_master_power
        self.fr = -self.front_master_power
        self.bl = -self.back_master_power
        self.br = -self.back_master_power
        self.move()

    def left(self):
        print("moving left")
        self.fl = -2*self.front_master_power
        self.fr = 2*self.front_master_power
        self.bl = 2*self.back_master_power
        self.br = -2*self.back_master_power
        self.move()

    def right(self):
        print("moving right")
        self.fl = 2*self.front_master_power
        self.fr = -2*self.front_master_power
        self.bl = -2*self.back_master_power
        self.br = 2*self.back_master_power
        self.move()

    def stop(self):
        print("stopping")
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.move()

    def braking(self):
        print('Braking')
        self.fl = BRAKE
        self.fr = BRAKE
        self.bl = BRAKE
        self.br = BRAKE

    def movement_test(self):
        print("starting movement test")
        for i in range (0, 3):
            if i == 0:
                self.slow()
            elif i == 1:
                self.medium()
            else:
                self.fast()
            self.forwards()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.backwards()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.left()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.right()
            time.sleep(2)
            self.stop()
            time.sleep(1)

    def forwards_test(self):
        self.forwards()
        time.sleep(2)
        self.stop()
        time.sleep(1)

    def marker(self):
        self.markers = self.camera.see()

    def marker_ids(self):
        self.markers = self.camera.see_ids()
    
    def marker_test(self):
        print("starting marker test")
        while True:
            markers = self.camera.see()
            print("I can see", len(markers), "markers:")
            if markers:self.chase_the_markers_advanced()
                self.forwards_test()
            for m in markers:
                print(" - Marker #{0} is {1} metres away".format(m.id, m.distance))

    def chase_the_marker(self):
        print('Playing chase the marker')
        while True:
            markers = self.camera.see()
            if markers:
                while markers[0].distance > 1000:
                    self.medium()
                    self.forwards()
                    markers = self.camera.see()
                    if not markers:
                        self.stop()
                        break
                self.stop()

    def find_the_angle(self):
        for i in range(0, 50):
            markers = self.camera.see()
            if markers:
                print(markers[0].spherical)

    def chase_the_markers_advanced(self):
        moving = ''
        while True:
            markers = self.camera.see()
            if markers:
                while markers[0].distance > 500:
                    print((markers[0].spherical))
                    print((markers[0].spherical)[0])
                    print((markers[0].spherical)[1])
                    if ((markers[0].spherical)[1]) < 0.1 and ((markers[0].spherical)[1]) > -0.1:
                        if moving == 'forwards':
                            self.fast()
                            self.forwards()
                            time.sleep(0.2)
                        else:
                            self.stop()
                            time.sleep(0.2)
                            self.fast()
                            self.forwards()
                            time.sleep(0.2)
                            moving = 'forwards'
                        markers = self.camera.see()
                        if not markers:
                            self.stop()
                            time.sleep(0.2)
                            break

                    elif ((markers[0].spherical)[1]) > 0.1:
                        if moving == 'left':
                            self.medium()
                            self.left()
                            time.sleep(0.2)
                        else:
                            self.stop()
                            time.sleep(0.2)
                            self.medium()
                            self.left()
                            time.sleep(0.2)
                            moving = 'left'
                        markers = self.camera.see()
                        if not markers:
                            self.stop()
                            time.sleep(0.2)
                            break

                    else:
                        if moving == 'right':
                            self.medium()
                            self.right()
                            time.sleep(0.2)
                        else:
                            self.stop()
                            time.sleep(0.2)
                            self.medium()
                            self.right()
                            time.sleep(0.2)
                            moving = 'right'
                        markers = self.camera.see()
                        if not markers:
                            self.stop()
                            time.sleep(0.2)
                            break
                self.stop()
                time.sleep(0.2)

    def angle_testing(self):
        while True:
            markers = self.camera.see()
            if markers:
                if ((markers[0].spherical)[1]) > 0:
                    self.fast()
                    self.forwards()
                    time.sleep(0.25)
                    self.stop()
                if ((markers[0].spherical)[1]) < 0:
                    self.fast()
                    self.backwards()
                    time.sleep(0.25)
                    self.stop()

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
    
    # def servo_test(self):
    #     self.medium()
    #     self.servo.position=1
    #     time.sleep(5)
    #     self.servo.position=-1
    #     time.sleep(5)
    #     #self.spin_servo_clockwise()

    # def spin_servo_clockwise(self,rotations):
    #     for i in range(rotations):
    #         self.servo.position=1
    #         time.sleep(1)
    def can_Regonition(self):
        while True:
            success,img = self.cap.read()
            classIds,confs,bbox = self.net.detect(img,confThreshold=0.25)
            if len(classIds) >= 1:
                for classId,confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    can = self.classNames[classId-1]
                    self.confs1 = confs
                    self.img1 = img
                    self.box1 = box
                    boxy = np.array_str(box)
                    coords = boxy.replace(' ', ',')
                    formatted = coords.replace('[','')
                    fullyformatted = formatted.replace(']','')
                    self.boxposition = box
                    #if can == "bottle":
                        #print("I found something useful")
                        #print(can)
                        #print(fullyformatted)
                        #cv2.rectangle(img,box,color=(0,255,0),thickness = 2)
                        #self.where_CanX()
                        #self.where_CanY()
                    if can == "bowl":
                        print("I found a can")
                        #print(fullyformatted)
                        self.where_CanX()
                        self.where_CanY()
                    elif can == "cup":
                        print("I found a can")
                        print(fullyformatted)
                        self.where_CanX()
                        self.where_CanY()
                    #elif can == "cell phone":
                        #print("I found something useful")
                        #print(can)
                        #print(fullyformatted)
                        #self.where_CanX()
                        #self.where_CanY()
                    else:
                        pass
            cv2.imshow("Can Detector",img)
            cv2.waitKey(1)
    def where_CanX(self):
        print(self.boxposition)
        if self.boxposition[0] >= 450:
            print("going left!")
        elif self.boxposition[0] >= 250 and self.boxposition[0] <= 450:
            print("in the centre")
        elif self.boxposition[0] <= 250:
            print("going right!")
    def where_CanY(self):
        if self.boxposition[3] > 300:
            print("getting closer!")
            self.DrawLines()
        elif self.boxposition[3] < 300 and self.boxposition[3] > 60: 
            print("getting further away")
            self.DrawLines()
        else:
            print("object detected is too far away.")
    def DrawLines(self):
        #7print(self.confs1)
        #if self.confs1 > 0.19:
        cv2.rectangle(self.img1,self.box1,color=(0,255,0),thickness = 10)
        print(self.box1)

    def start(self):
        self.power_H1()
        self.power_H0()
        self.power_L0()
        self.can_Regonition()
        self.chase_the_markers_advanced()
        #self.movement_test()
        #self.servo_test()
        #self.marker_test()
        #self.chase_the_marker()
        #self.find_the_angle()
        #self.angle_testing()
def main():
    jeff = Collybot()
    jeff.start()
if __name__ == '__main__':
    main()