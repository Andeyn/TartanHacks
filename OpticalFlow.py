import numpy as np
import cv2
import copy

def getWebcam():
    webcam = cv2.VideoCapture(0)
    #Frame coordinates go frame[y][x]
    while True:
        ret, frame = webcam.read()
        lowFiFrame = cv2.resize(copy.deepcopy(frame), (0,0), fy=.5, fx=.5)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
    
getWebcam()
print("winnie saw this")