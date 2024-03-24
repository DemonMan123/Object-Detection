import cv2 as cv
import numpy as np
import cvlib as cvl
from cvlib.object_detection import draw_bbox
import pyfirmata as pym
import threading
from threading import Lock

board = pym.ArduinoMega('COM3')
Servo = board.get_pin('d:8:s')
servo_lock = Lock()
board.digital[13].write(1)
print("Arduino active..")

Servo.write(0)

global_servo_position = 90


def CheckForPerson(label, conf, bbox, center_x):
    global global_servo_position
    if label == 'person':
        bbox_x, bbox_y, width, height = bbox[0]
        distance_from_center = bbox_x - center_x
        
        print("{:.2f}".format(conf), label)
        print(f"X: {bbox_x}\nWidth: {width}\n")
        print(f"Distance from center: {distance_from_center}")
        with servo_lock:
            if distance_from_center > 20:
                global_servo_position += 3
            elif distance_from_center < -20:
                global_servo_position -= 3
        
        global_servo_position = max(0, min(180, global_servo_position))
        with servo_lock:  
                print(f"Adjusted Servo Position: {global_servo_position}")
                Servo.write(global_servo_position)  # Move the servo to the new position
    else:
        pass

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()  # Frame size is (480, 640, 3)
    
    F_height, F_width = frame.shape[:2]

    center_x = F_width // 2

    bbox, labels, conf = cvl.detect_common_objects(frame)

    if labels:
        for confidence, label, box in zip(conf, labels, bbox):
            print(box)
            CheckForPersonThread = threading.Thread(target=CheckForPerson, args=(label, confidence, [box], center_x))
            CheckForPersonThread.daemon = True
            CheckForPersonThread.start()
            draw_bbox(frame, bbox, labels, conf)

    cv.imshow("Video", frame)

    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
Servo.write(90)  # Reset servo to center position
print("Arduino inactive..")
board.digital[13].write(0)