import RPi.GPIO as GPIO
import time
from threading import Thread, Event, Lock
from Motor import *
from Ultrasonic import *
from Line_Tracking import *


class CombinedLineTrackingAndUltrasonic:
    def __init__(self):
        self.ultrasonic = ultrasonic
        self.line_tracking = infrared
        self.stop_event = Event()
        self.distance_lock = Lock()
        self.distance = 0
        self.stop_event.set()  # Initially, the event is set to allow line tracking to run

    def ultrasonic_thread(self):
        while True:
            distance = self.ultrasonic.get_distance()

            with self.distance_lock:
                self.distance = distance

            # print("Distance:", distance, "cm")
            if distance < 50:  # Stop the robot if an obstacle is detected within 50 cm
                self.stop_event.clear()
                PWM.setMotorModel(0, 0, 0, 0)
            else:
                if not self.stop_event.set():
                    self.stop_event.set()
                    PWM.setMotorModel(800, 800, 800, 800)
            time.sleep(0.1)

    def line_tracking_thread(self):
        while True:
            self.stop_event.wait()  # wait until event is set
            line_tracking_result = self.line_tracking.run()
            with self.distance_lock:
                distance = self.distance
            print(f"Line Tracking: {line_tracking_result}, Distance: {distance} cm")
            time.sleep(0.1)

    def run(self):
        ultrasonic_thread = Thread(target=self.ultrasonic_thread)
        line_tracking_thread = Thread(target=self.line_tracking_thread)
        ultrasonic_thread.start()
        line_tracking_thread.start()
        ultrasonic_thread.join()
        line_tracking_thread.join()


if __name__ == '__main__':
    robot = CombinedLineTrackingAndUltrasonic()
    robot.run()
