import cv2
import numpy as np


def threshold(image):
    # 1. convert to hsv space, config match black since that's our lane
    imageHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blackLowerRange = np.array([30, 125, 0], dtype="uint8")
    blackUpperRange = np.array([170, 255, 255], dtype="uint8")

    blackMask = cv2.inRange(imageHsv, blackLowerRange, blackUpperRange)
    return blackMask


def warpImage(image, points, width, height, inverse=False):
    point1 = np.float32(points)
    point2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    if inverse:
        matrix = cv2.getPerspectiveTransform(point2, point1)
    else:
        matrix = cv2.getPerspectiveTransform(point1, point2)

    imageWarp = cv2.warpPerspective(image, matrix, (width, height))

    return imageWarp


def nothing(a):
    pass


def initializeTrackbars(intialTrackbarVals, widthTarget=640, heightTarget=480):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTrackbarVals[0], widthTarget // 2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTrackbarVals[1], heightTarget, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTrackbarVals[2], widthTarget // 2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTrackbarVals[3], heightTarget, nothing)


def getTrackbarValues(widthTarget=640, heightTarget=480):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (widthTarget - widthTop, heightTop),
                         (widthBottom, heightBottom), (widthTarget - widthBottom, heightBottom)])
    return points


def getHistogram(image, minimumPercentage=0.1, display=False, region=1):

    if region == 1:
        values = np.sum(image, axis=0)  # sum pixel image
    else:
        values = np.sum(image[image.shape[0]//region:,:], axis=0)  # sum pixel given particular region

    maximum = np.max(values)
    minimum = minimumPercentage * maximum  # filters out noise and decides a path
                                            # 0.1 above 10 percent is path, below is noise

    indexList = np.where(values >= minimum) # List of values > minimum
    basePoint = int(np.average(indexList))
    # print(basePoint)

    if display:
        imageHistogram = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
        for x, intensity in enumerate(values):
            # show how many pixels are on and off
            if intensity > minimum:
                color = (255, 0, 255)
            else:
                color = (0, 255, 255)

            cv2.line(
                imageHistogram,
                (x, image.shape[0]),
                (x, int(image.shape[0] - intensity//255//region)),
                color,
                1
            )
            cv2.circle(
                imageHistogram,
                (basePoint, image.shape[0]),
                20,
                (0, 255, 255),
                cv2.FILLED
            )
        return basePoint, imageHistogram

    return basePoint



def drawPoints(image, points):
    for x in range(0, 4):
        cv2.circle(
            image,
            (int(points[x][0]),
             int(points[x][1])),
            15, (0, 0, 255),
            cv2.FILLED
        )
    return image


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver