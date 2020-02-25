import time
import picamera

def capture():
    with picamera.PiCamera() as camera:
        camera.resolution = (256, 176)

        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture('/tmp/capture.jpg', use_video_port=True)
        camera.stop_preview()
        camera.close()
if __name__ == '__main__':
    capture()
