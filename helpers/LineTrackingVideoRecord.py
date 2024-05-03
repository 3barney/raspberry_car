from Motor import *
from VideoCapture import *
import RPi.GPIO as GPIO
import time


class LineTrackingVideoRecord:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def run(self):
        video_capture.record_video()

        while True:
            self.LMR = 0x00
            if GPIO.input(self.IR01) == True:
                self.LMR = (self.LMR | 4)
            if GPIO.input(self.IR02) == True:
                self.LMR = (self.LMR | 2)
            if GPIO.input(self.IR03) == True:
                self.LMR = (self.LMR | 1)

            # 4, 2, 1 -> Rep left, Middle, Right
            # 3 (2+1), 6 (4+2), 7(4+2+1) -> Not valid since Lane is Large
            if self.LMR == 2:
                PWM.setMotorModel(500, 500, 500, 500)
                # PWM.setMotorModel(800, 800, 800, 800)
            elif self.LMR == 4:
                PWM.setMotorModel(-500, -500, 1000, 1000)
                # PWM.setMotorModel(-1500, -1500, 2500, 2500)
            elif self.LMR == 6:
                PWM.setMotorModel(500, 500, 500, 500)
                # PWM.setMotorModel(800, 800, 800, 800)
            elif self.LMR == 1:
                PWM.setMotorModel(1000, 1000, -500, -500)
                # PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR == 3:
                PWM.setMotorModel(500, 500, 500, 500)
                # PWM.setMotorModel(800, 800, 800, 800)
            elif self.LMR == 7:
                PWM.setMotorModel(0, 0, 0, 0)


infrared = LineTrackingVideoRecord()
# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        video_capture.stop_and_save()
        PWM.setMotorModel(0, 0, 0, 0)