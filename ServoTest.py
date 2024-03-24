import pyfirmata as pym
import cv2 as cv
import numpy as np
board = pym.ArduinoMega('COM3')
Servo = board.get_pin('d:8:s')
cv.namedWindow('Servo Selector')

Servo.write(0)
def MoveServo(x):
    Servo.write(x)

img = np.zeros((300,512,3), np.uint8)
cv.createTrackbar('Pos','Servo Selector',0,150,MoveServo)

while True:
    cv.imshow("Servo Selector",img)
    ServoPos = cv.getTrackbarPos('Pos','Servo Selector')
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break