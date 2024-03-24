import cv2 as cv
import numpy as np
import cvlib as cvl
from cvlib.object_detection import draw_bbox
import pyfirmata as pym
Salt = "Media/SALT.png"
BlurrySalt = "Media/BlurrySalt.png"
Salt_Temp = cv.imread(BlurrySalt,0)

confidence = 0.85
board = pym.ArduinoMega('COM3')
Servo = board.get_pin('d:8:s')
ServoPos = 0

def MoveServo(x):
    ServoPos = x
    Servo.write(ServoPos)

cap = cv.VideoCapture(0)
'''frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
center_x = frame_width // 2
center_y = frame_height // 2'''

board.digital[13].write(1)
print("Arduino active..")

img = np.zeros((300,512,3), np.uint8)

#cv.namedWindow('Servo Selector')
#cv.createTrackbar('Pos','Servo Selector',0,180,MoveServo)

while cap.isOpened():
    # A little code to be able to move servo manually
    #ServoPos = cv.getTrackbarPos('Pos','Servo Selector')
    
    ret, frame = cap.read() # Frame size is (480, 640, 3)
    F_height, F_width = frame.shape[:2]
    
    center_x = F_width // 2
    center_y = F_height // 2
    
    #cv.line(frame, (center_x, 0), (center_x, F_height), (0, 255, 0), 1)
    #cv.line(frame, (0, center_y), (F_width, center_y), (0, 255, 0), 1)
    #cv.circle(frame,(center_x,center_y),5,(255,0,0),1)
    
    
    if not ret:
        print("Can't get frame.")
        break
    '''
    faces, conf = cvl.detect_face(frame)
    print(conf)
    for face, confidences in zip(faces,conf):
        (startX,startY) = face[0],face[1]
        (endX,endY) = face[2],face[3]
        cv.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
    '''
    bbox, labels, conf = cvl.detect_common_objects(frame)
    if labels:
        for confidence,label in zip(conf,labels):
            if label == 'person':
                bbox_x, bbox_y, width, height = bbox[0]
                print("{:.2f}".format(confidence),label)
                print(f"X: {bbox_x}\nY: {bbox_y}\nWidth: {width}\nHeight: {height}")
                ServoPos = ServoPos+5
                if ServoPos <= 180:
                    Servo.write(ServoPos)
                    pass
                else:
                    ServoPos = 0
                    Servo.write(ServoPos)
                    pass
            draw_bbox(frame,bbox,labels,conf)
    '''
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray, Salt_Temp, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    for pt in zip(*loc[::-1]):
        h, w = Salt_Temp.shape[:2]
        cv.rectangle(frame, (pt[0]+1, pt[1]), (pt[0]+w-2, pt[1]+h-40), (230, 38, 0), 2)
    '''
    cv.imshow("Video",frame)
    #cv.imshow("Servo Selector",img)
    if cv.waitKey(1) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows
Servo.write(0)
print("Arduino inactive..")
board.digital[13].write(0)