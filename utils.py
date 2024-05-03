import cv2
import numpy as np

def threshold(image):
    # 1. convert to hsv space

    imageHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blackLowerRange = np.array([30, 125, 0], dtype="uint8")
    blackUpperRange = np.array([170, 255, 255], dtype="uint8")  # Correct config for light and dark room # 50,50,50 DARK

    blackMask = cv2.inRange(imageHsv, blackLowerRange, blackUpperRange)
    return blackMask
