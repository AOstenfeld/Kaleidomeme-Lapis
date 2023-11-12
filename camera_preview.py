from picamera import PiCamera
from time import sleep
import keyboard

camera = PiCamera()
def video():
    camera.start_preview()
    camera.preview_fullscreen = False
    camera.preview.window = (300, 200, 1920, 1080)
    sleep(5)
    camera.stop_preview()

while True:
    if keyboard.is_pressed("p"):
        print('i pressed p')
        break
