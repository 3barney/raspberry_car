import cv2
import numpy as np
from tensorflow.keras.models import load_model
import data_capture.line_tracking
from data_capture.image_capture import *
from data_capture.Motor import *

model = load_model('/home/pi/Desktop/My Files/RpiRobot/model.keras')


def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


image_capture = ImageCapture(resolution=(240, 120))

while True:
    steering_input = np.array([0.0, 0.0, 0.0])
    steering_input = np.expand_dims(steering_input, axis=0)

    img = image_capture.capture_image()
    img = np.asarray(img)
    img = preProcess(img)
    # img = np.array([img])
    img = np.expand_dims(img, axis=0)

    prediction = model.predict({'image_input': image, 'numerical_input': steering_input})
    print(f'Prediction for the test image: {prediction}')
    if prediction < 0.33:
        PWM.setMotorModel(-300, -300, 700, 700)
        # return 'left'
    elif prediction < 0.66:
        PWM.setMotorModel(300, 300, 300, 300)
        # return 'forward'
    else:
        PWM.setMotorModel(700, 700, -300, -300)
        # return 'right'
