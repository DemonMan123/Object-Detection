# Facial detection turret program, written by Demin (Unfinished)
import cv2 as cv
import cvlib as cvl
import threading
from Get_Centers import getCenter_rectangle,GetCenter_frame
import pyfirmata as pym
import numpy as np

ServoX_pin = 8 # Servo X pin on board
ServoY_pin = 9 # Servo Y pin on board

board = pym.ArduinoMega('COM3')
Servo = board.get_pin(f'd:{ServoX_pin}:s') # Sets up the servo pin X
Servo = board.get_pin(f'd:{ServoY_pin}:s') # Sets up the servo pin Y
board.digital[13].write(1)
print("Arduino active..")

global_servo_positionX = 90
global_servo_positionY = 90
global_position_tolerance = 0

cv.namedWindow('Tolerance Selector')
TolWin = np.zeros((50,512,3), np.uint8)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    exit("Unable to open camera..")

def GetToleranceLimit(Tolerance):
    print(Tolerance)

def moveServoX(posX):
    print(f"Ran moveServoX {posX}")
    Servo.write(posX)

def moveServoY(posY):
    print(f"Ran moveServoY {posY}")
    Servo.write(posY)

def DetectObj(frame):
    global global_servo_positionX
    global global_servo_positionY
    F_height, F_width = frame.shape[:2] # Gets the width/height of the frame
    center_y,center_x = GetCenter_frame(F_height,F_width) # Gets the center of the frame

    faces, conf = cvl.detect_face(frame)
    if faces:
        for idx, f in enumerate(faces): # Creates an array for faces (f), IDX is ignored.
            (startX, startY) = f[0], f[1] # Starting points for X/Y
            (endX, endY) = f[2], f[3] # Ending points for X/Y
            rectx,recty = getCenter_rectangle(startX,startY,endX,endY) # Gets the center of a rectangle given a certain width/height
            rectcenter = int(rectx),int(recty)
            diffx = abs(int(rectx) - center_x) # Gets the absolute (Aka no negative) value of X
            diffy = abs(int(recty) - center_y) # Gets the absolute value of Y
            
            if diffx <= global_position_tolerance:
                print("Aligned on X axis")
            else:
                if int(rectx) > center_x:
                    global_servo_positionX -= 1
                elif int(rectx) < center_x:
                    global_servo_positionX += 1
            
            if diffy <= global_position_tolerance:
                print("Aligned on the Y axis")
            else:
                if int(recty) > center_y:
                    global_servo_positionY += 1
                elif int(recty) < center_y:
                    global_servo_positionY -= 1
                    
            if diffx and diffy <= global_position_tolerance:
                print("Both aligned")
                
            global_servo_positionX = max(0, min(180, global_servo_positionX))
            global_servo_positionY = max(0, min(180, global_servo_positionY))
            cv.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
            cv.circle(frame,rectcenter,global_position_tolerance,(0,255,0),2)
            cv.line(frame, (center_x, 0), (center_x, F_height), (0, 255, 0), 1)
            cv.line(frame, (0, center_y), (F_width, center_y), (0, 255, 0), 1)
            
            threads = [
                threading.Thread(target=moveServoX(global_servo_positionX)),
                threading.Thread(target=moveServoY(global_servo_positionY))
            ]
            for th in threads:
                th.start()
            for th in threads:
                th.join()

cv.createTrackbar('Tolerance','Tolerance Selector',0,150,GetToleranceLimit)

def Show_Cap():
    global global_position_tolerance
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            exit("Unable to read video feed")
        
        cv.imshow("Tolerance Selector",TolWin)
        global_position_tolerance = cv.getTrackbarPos('Tolerance','Tolerance Selector')
        
        threading.Thread(target=DetectObj(frame)).start()
        cv.imshow("Video", frame)
        if cv.waitKey(1) == ord("q"):
            break

threading.Thread(target=Show_Cap()).start()
cap.release()
cv.destroyAllWindows()
