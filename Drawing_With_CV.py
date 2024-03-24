import numpy as np
import cv2 as cv

img = np.zeros((512,512,3), np.uint8)

# cv.line(img,(511,400),(0,0),(255,0,0),5) Takes the arguments: ImageName, StartPOS, EndPOS, Color, Thickness
# cv.rectangle(img,(384,0),(510,128),(0,255,0),-1) Takes the arguments: ImageName, Top Left corner, Top Right corner, Color, Thickness
# cv.circle(img,(447,63), 63, (0,0,255), -1) Takes the arguments: Center Coordinates, Radius, Color, Thickness
# cv.ellipse(img,(256,256),(100,50),0,0,180,255,-1) Takes the arguments: Center location, Axes Lengths (Major and Minor), Angle of Rotation, Start angle, End angle, Opacity/Color?, thickness
# font = cv.FONT_HERSHEY_SIMPLEX Specifies font
# cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA) Takes in 8 parameters: ImageName, start pos for text, Font, Font Size, Color, Line Thickness, and Line Type (LINE_AA = Anti-aliasing)

# Making a smiley face..
font = cv.FONT_HERSHEY_SIMPLEX
cv.circle(img, (230,255),15,(255,0,0),2) # Left Eye
cv.circle(img, (280,255),15,(255,0,0),2) # Right Eye

cv.circle(img, (235,257),4,(0,0,255),2) # Left Eye Center
cv.circle(img, (278,257),4,(255,0,255),2) # Right Eye Center

cv.ellipse(img,(256,256),(100,50),0,0,180,255,15) # Smile
cv.putText(img,'Smile',(80,450), font, 4,(255,255,255),2,cv.LINE_AA)


while True:
    cv.imshow("Result", img)
    if cv.waitKey(1) == ord("q"):
        break

cv.destroyAllWindows