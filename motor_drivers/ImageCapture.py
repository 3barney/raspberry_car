from picamera2 import Picamera2, Preview

import cv2


class ImageCapture:

    def __init__(self, resolution=(1920, 1080)):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration(main={"size": resolution})
        self.picam2.configure(camera_config)

    def capture_image(self, display=False):
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        image = self.picam2.capture_array()
        img = cv2.resize(image, (480, 240))
        if display:
            cv2.imshow("image", img)

        return img

    def stop(self):
        self.picam2.stop_preview()
        self.picam2.stop()


camera_capture = ImageCapture(resolution=(980, 600))

if __name__ == '__main__':
    try:
        image = camera_capture.capture_image(display=True)
    except KeyboardInterrupt:
        print("Camera stopped")
    finally:
        camera_capture.stop()