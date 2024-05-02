from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

import time

class VideoCapture:

    def __init__(self, output_file, resolution=(1920, 1080), bitrate=10000000):
        self.picam2 = Picamera2()
        video_config = self.picam2.create_video_configuration(main={"size": resolution})
        self.picam2.configure(video_config)
        self.encoder = H264Encoder(bitrate=bitrate)
        self.output_file = output_file

    def record_video(self):
        self.picam2.start_preview(Preview.QTGL)  # pi specific, not needed on desktop
        self.picam2.start_recording(self.encoder, self.output_file)
        print("Recording or performing operations. Press Ctrl+C to stop.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Recording stopped by user")
        finally:
            self.stop_and_save()


    def stop_and_save(self):
        self.picam2.stop_recording()
        self.picam2.stop_preview()
        self.picam2.stop()
        print(f"Video saved to {self.output_file}")


video_capture = VideoCapture(output_file="/home/barneyjomo/pi/video.mp4", resolution=(640, 360))

if __name__ == '__main__':
    # video_capture = VideoCapture(output_file="/home/pi/video.mp4", resolution=(640, 360))

    try:
        video_capture.record_video()
    except KeyboardInterrupt:
        print("Recording Stopped by user")
    finally:
        # Stop recording and preview
        video_capture.stop_and_save()

