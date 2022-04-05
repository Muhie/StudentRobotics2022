from sr.robot3 import *
import cv2
import numpy as np
class Collybot(Robot):
    def __init__(self):
        super().__init__()
        self.classNames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']
        path = str(self.usbkey)
        self.path1 = path
        self.weightsPath = path+"/frozen_inference_graph.pb"
        self.configPath =path+"/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        print(self.weightsPath,self.configPath)
        self.net = cv2.dnn_DetectionModel(self.weightsPath,self.configPath)
        self.net.setInputSize(200,200)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)
        self.marker_ids = self.camera.save(self.usbkey / "initial-view.png")
    def can_Regonition(self):
        img = cv2.imread(self.path1+"initial-view.png")
        while True:
            #success,img = self.cap.read()
            classIds,confs,bbox = self.net.detect(img,confThreshold=0.4)
            #if len(classIds) >= 1:
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
                elif can == "cell phone":
                    print("I found something useful")
                    print(can)
                    print(fullyformatted)
                    self.where_CanX()
                    self.where_CanY()
                else:
                    pass
            cv2.imshow("Can Detector",img)
            cv2.waitKey(0)
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

                    


def main():
    jeff = Collybot()
    jeff.can_Regonition()
if __name__ == '__main__':
    main()
