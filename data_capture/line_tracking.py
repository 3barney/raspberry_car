import time

import RPi.GPIO as GPIO
from Motor import *

class LineTracking:

    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def get_turn_value(self):
        self.LMR = 0x00
        if GPIO.input(self.IR01):
            self.LMR = (self.LMR | 4)
        if GPIO.input(self.IR02):
            self.LMR = (self.LMR | 2)
        if GPIO.input(self.IR03):
            self.LMR = (self.LMR | 1)
        if self.LMR == 2:
            # Middle active
            PWM.setMotorModel(200, 200, 200, 200)
            return "forward"
        elif self.LMR == 4:
            # Left active
            PWM.setMotorModel(-200, -200, 700, 700)
            return "left"
        elif self.LMR == 1:
            # Right active
            PWM.setMotorModel(700, 700, -200, -200)
            return "right"
        elif self.LMR == 7:
            # Stop
            PWM.setMotorModel(0, 0, 0, 0)
            return "stop"
        elif self.LMR == 6:
            PWM.setMotorModel(-400, -400, 1000, 1000)
            return "left"
        elif self.LMR == 3:
            PWM.setMotorModel(1000, 1000, -400, -400)
            return "right"
        return "forward"


# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        infrared = LineTracking()
        infrared.get_turn_value()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0, 0, 0, 0)
