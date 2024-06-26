import logging
from threading import Thread, Event, Lock

import data_collection_module
import line_tracking
from image_capture import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
            try:
                turn_value = self.line_tracking.get_turn_value()
                logging.info(f"line_tracking_thread {turn_value}")
                with self.lock:
                    self.turn_value = turn_value
                time.sleep(0.1)
            except Exception as e:
                logging.error(f"Error in line tracking thread: {e}")

    def camera_capture_thread(self):
        while not self.stop_event.is_set():
            try:
                with self.lock:
                    turn_value = self.turn_value

                img_data = self.image_capture.capture_image(display=True)
                logging.info(f"Captured and saved image: {turn_value}")
                data_collection_module.saveData(img_data, turn_value)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error in camera capture thread: {e}")

    def run(self):
        try:
            line_tracking_thread = Thread(target=self.line_tracking_thread)
            camera_capture_thread = Thread(target=self.camera_capture_thread)
            line_tracking_thread.start()
            camera_capture_thread.start()

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            data_collection_module.saveLog()
            self.stop_event.set()
            line_tracking_thread.join()
            camera_capture_thread.join()
            logging.info("Data capture stopped")


if __name__ == '__main__':
    data_capture = DataCapture()
    data_capture.run()
