import time
import cv2
import numpy as np
from picamera2 import Picamera2

from helpers.Motor import *
from utils import *

if __name__ == '__main__':
    # TODO: We run test video that we will capture
    pass

# Initialize camera
# picam2 = Picamera2()
# camera_config = picam2.create_preview_configuration(main={"size": (640, 360)})
# picam2.configure(camera_config)
# time.sleep(5)
# picam2.start()
# time.sleep(0.1) # for camera to initialize
#
# try:
#     while True:
#         image = picam2.capture_array()
#
#         blackline = cv2.inRange(image, (0, 0, 0), (50, 50, 50))
#         img, contours, hierachy = cv2.find
#
# finally:
#     cv2.destroyAllWindows()
#     picam2.stop()
