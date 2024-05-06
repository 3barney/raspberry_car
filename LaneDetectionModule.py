import time
import cv2
import numpy as np
from cv2 import VideoCapture

import utils

curveList = []
avgValue = 10


def getLaneCurve(image, display=2):
    imageCopy = image.copy()
    imageResult = image.copy()

    # STEP 1. Threshold based on color since our path is black, just get black pixels : (Rsch Edge Detectors)
    imageThreshold = utils.threshold(image)

    # STEP 2
    initialTrackbar = [34, 248, 34, 412]
    utils.initializeTrackbars(initialTrackbar)

    height, width, channels = image.shape
    points = utils.getTrackbarValues()
    imageWarp = utils.warpImage(imageThreshold, points, width, height)
    imageWarpPoints = utils.drawPoints(imageCopy, points)

    # STEP 3
    middlePoint, imageHistogram = utils.getHistogram(imageWarp, minimumPercentage=0.5, display=True, region=4)
    curveAveragePoint, imageHistogram = utils.getHistogram(imageWarp, display=True, minimumPercentage=0.9)

    curveRawValue = curveAveragePoint - middlePoint

    # Step 4: Average to have smooth transition and not rapid value movement
    curveList.append(curveRawValue)
    if len(curveList) > avgValue:
        curveList.pop(0)

    curve = int(sum(curveList) / len(curveList))

    # STEP 5: display
    if display != 0:
        imgInvWarp = utils.warpImage(imageWarp, points, width, height, inverse=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:height // 3, 0:width] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imageResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (width // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (width // 2, midY), (width // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((width // 2 + (curve * 3)), midY - 25), (width // 2 + (curve * 3), midY + 25), (0, 255, 0),
                 5)
        for x in range(-30, 30):
            w = width // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imageWarpPoints, imageWarp],
                                             [imageHistogram, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    # cv2.imshow("Threshold", imageThreshold)
    # cv2.imshow("Image Warp", imageWarp)
    # cv2.imshow("Warp Points", imageWarpPoints)
    # cv2.imshow("Image histogram", imageHistogram)

    # Normalize [-1, 1]
    curve = curve / 100
    if curve > 1:
        curve == 1
    if curve < -1:
        curve == -1

    return curve


if __name__ == '__main__':

    capture = cv2.VideoCapture('videos/pi/evening/evening500_clockwise_1.mp4')
    initialTrackbar = [34, 248, 34, 412]
    utils.initializeTrackbars(initialTrackbar)
    frameCounter = 0

    while True:
        frameCounter += 1
        if capture.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = capture.read()  # GET THE IMAGE
        img = cv2.resize(img, (640, 480))  # RESIZE

        # DEBUG = 2, run = 0
        curve = getLaneCurve(img, display=2)
        # print(curve)
        curveValue = curve
        if curveValue > 0.3: curveValue = 0.3
        if curveValue < -0.3: curveValue = -0.3

        # CLOCKWISE -> TURN RIGHT
        # ANTICLOCKWISE -> TURN LEFT

        # if curveValue > 0:
        #     print("Turn Right")
        #     if curveValue < 0.05:
        #         curveValue = 0
        # else:
        #     if curveValue > -0.08:
        #         print("MOVE FORWARD")
        #         curveValue = 0

        # print(curveValue)

        # cv2.imshow('vid', img)
        cv2.waitKey(1)
