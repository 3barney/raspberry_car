import time
import cv2

from picamera2 import Picamera2, Preview


class ImageCapture:

    def __init__(self, resolution=(1920, 1080)):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration(main={"size": resolution})
        self.picam2.configure(camera_config)
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        time.sleep(2)

    def capture_image(self, display=False):
        image_data = self.picam2.capture_array()
        image_resize = cv2.resize(image_data, (480, 240))

        if display:
            cv2.imshow("captured image", image_resize)
            cv2.waitKey(1)

        return image_resize

    def stop(self):
        self.picam2.stop_preview()
        self.picam2.stop()
        cv2.destroyAllWindows()
        print("Stopping camera....")


if __name__ == '__main__':
    try:
        camera_capture = ImageCapture(resolution=(980, 600))
        image = camera_capture.capture_image(display=True)
    except KeyboardInterrupt:
        print("Camera stopped")
    finally:
        camera_capture.stop()
