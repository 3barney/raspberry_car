from motor_drivers.Motor import *
from LaneDetectionModule import getLaneCurve
from motor_drivers.ImageCapture import *

import cv2

def main():

    img = camera_capture.capture_image(display=True)
    curveValue = getLaneCurve(img, display=2)

    # print(f"curve value {curveValue}")

    if curveValue > 0.3 : curveValue = 0.3
    if curveValue < -0.3 : curveValue = -curveValue

    if curveValue > 0:
        print("Turn Right")
        PWM.setMotorModel(1000, 1000, -500, -500)
        if curveValue < 0.05:
            curveValue = 0
    else:
        if curveValue > -0.08:
            print("MOVE FORWARD")
            PWM.setMotorModel(500, 500, 500, 500)
            curveValue = 0

    # if curveValue > 0:
    #     print("Turn Right")
    #     PWM.setMotorModel(-500, -500, 1000, 1000)
    #
    #     if curveValue < 0.05:
    #         print("in here")
    #         curveValue = 0
    # else:
    #     if curveValue > -0.08: curveValue = 0
    cv2.waitKey(1)


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        camera_capture.stop()