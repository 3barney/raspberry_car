import sys
import os
import math
import time

from threading import Thread, Event, Lock
from image_capture import *
import data_collection_module
import line_tracking
# access the motor_driver package
# current_dir = os.path.dirname(__file__)
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

# import motor_drivers.line_tracking as line_tracking


class DataCapture:

    def __init__(self):
        # No need for ultrasonic during image capture
        self.image_capture = ImageCapture(resolution=(980, 600))
        self.line_tracking = line_tracking.LineTracking()
        self.stop_event = Event()
        self.lock = Lock()
        self.turn_value = None

    def line_tracking_thread(self):
        while not self.stop_event.is_set():
            turn_value = self.line_tracking.get_turn_value()
            print(f"line_tracking_thread {turn_value}")
            with self.lock:
                self.turn_value = turn_value
            time.sleep(0.1)

    def camera_capture_thread(self):
        while not self.stop_event.is_set():
            with self.lock:
                turn_value = self.turn_value

            img_data = self.image_capture.capture_image(display=True)
            print(f"camera_capture_thread saving data with {turn_value}")
            data_collection_module.saveData(img_data, turn_value)
            time.sleep(1)

    def run(self):
        line_tracking_thread = Thread(target=self.line_tracking_thread())
        camera_capture_thread = Thread(target=self.camera_capture_thread())
        line_tracking_thread.start()
        camera_capture_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Killing application")
            data_collection_module.saveLog()
            self.stop_event.set()
            line_tracking_thread.join()
            camera_capture_thread.join()


if __name__ == '__main__':
    data_capture = DataCapture()
    data_capture.run()
