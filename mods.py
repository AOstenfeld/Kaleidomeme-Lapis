#Contains custom classes for operating the camera and motor
import RPi.GPIO as GPIO
from time import sleep
import threading

class Motor:

    def __init__(self, pins, delay, run=False, ccw=True):
        self.pins = pins
        self.delay = delay
        self.run = run
        self.ccw = ccw
        self.ccw_steps_logic = [[1, 1, 0, 0],
                                [1, 0, 0, 1],
                                [0, 0, 1, 1],
                                [0, 1, 1, 0]]
        self.cw_steps_logic = [[1, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 1, 1],
                               [1, 0, 0, 1]]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT)

    def set_delay(self, delay):
        self.delay = delay

    def set_run(self, run):
        self.run = run

    def set_ccw(self, ccw):
        self.ccw = ccw

    def clean(self):
        GPIO.cleanup(self.pins)

    def read_states(self, states):
        GPIO.output(self.pins, states)

    def ccw_cycle(self, cycles=1):
        for j in range(len(self.ccw_steps_logic)):
            self.read_states(self.ccw_steps_logic[j])
            sleep(self.delay)

    def cw_cycle(self, cycles=1):
        for j in range(len(self.cw_steps_logic)):
            self.read_states(self.cw_steps_logic[j])
            sleep(self.delay)

    def cycle(self, cycles=1):
        if self.run:
            for i in range(0, cycles):
                if self.ccw:
                    self.ccw_cycle()
                else:
                    self.cw_cycle()

class Screenshot:

    def __init__(self, picFile="pic#0#.jpg",vidFile = "vid#0#.h264"):
        self.picFile = picFile
        self.vidFile = vidFile

    def vid(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24

        camera.start_preview()
        camera.preview_fullscreen = False
        camera.preview.window = (300, 200, 1920, 1080)
        camera.start_recording("Videos/" + self.vidFile)
        camera.wait_recording(5)
        camera.stop_recording()
        camera.stop_preview()
        tmp = self.vidFile.split('#')
        tmp[1] = str(int(tmp[1]) + 1)
        self.vidFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.close()

    def pic(self):
        camera = PiCamera()
        camera.resolution = (1024,768)
        camera.start_preview(alpha=200)
        sleep(2)
        camera.capture("Screenshots/" + self.picFile)
        camera.stop_preview()
        tmp = self.picFile.split('#')
        tmp[1] = str(int(tmp[1]) + 1)
        self.picFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.close()

class KalThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(KalThread, self).__init__(*args, **kwargs)
        self.go = threading.Event()

    def go(self):
        self.go.set()

    def stop(self):
        self.go.clear()

    def check_flag(self):
        return self.go.is_set()
