import time
import cv2
import numpy as np
import utils

def getLaneCurve(img):
    # recieve an image and returns value of curve

    # 1. Threshold based on color since our path is black, just get black pixels : (Rsch Edge Detectors)

    imageThreshold = utils.threshold(img)

    cv2.imshow("Threshold", imageThreshold)
    return None


if __name__ == '__main__':

    cap = cv2.VideoCapture('videos/pi/daytime/daytime500_clockwise_1.mp4')
    while True:
        success, img = cap.read()  # GET THE IMAGE
        img = cv2.resize(img, (640, 480))  # RESIZE

        getLaneCurve(img)
        cv2.imshow('vid', img)
        cv2.waitKey(1)

