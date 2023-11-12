from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

camera.start_preview()
camera.preview_fullscreen = False
camera.preview.window = (300, 200, 1920, 1080)
camera.start_recording("testvid.h264")
camera.wait_recording(5)
camera.stop_recording()
camera.stop_preview()
