import cv2

#img = cv2.imread("lena.PNG")
cap = cv2.VideoCapture(0)
cap.set(3,240)
cap.set(4,180)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 10)
classNames = []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")
    
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)
while True:
    success,img = cap.read()
    classIds,confs,bbox = net.detect(img,confThreshold=0.55)
    if len(classIds) != 0:
        for classId,confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            can = classNames[classId-1]
            if can == "cup":
                print("I found something useful")
                print(can)
                cv2.rectangle(img,box,color=(0,255,0),thickness = 2)
            elif can == "bowl":
                print("I found something useful")
                print(can)
                cv2.rectangle(img,box,color=(0,255,0),thickness = 2)
            elif can == "bottle":
                print("I found something useful")
                print(can)
                cv2.rectangle(img,box,color=(0,255,0),thickness = 2)
            elif can == "cell phone":
                print("I found something useful")
                print(can)
                cv2.rectangle(img,box,color=(0,255,0),thickness = 2)
            else:
                pass
                

    cv2.imshow("Bottle Detector",img)
    cv2.waitKey(300)