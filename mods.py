#Contains custom classes for operating the camera and motor
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

class KalMotor:

    def __init__(self, pins, delay, ccw=True):
        self.pins = pins #[a1, b1, a2, b2]
        self.delay = delay
        self.ccw = ccw
        self.ccw_steps_logic = [[1, 1, 0, 0],
                                [1, 0, 0, 1],
                                [0, 0, 1, 1],
                                [0, 1, 1, 0]]
        self.cw_steps_logic = [[1, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 1, 1],
                               [1, 0, 0, 1]]

    def set_delay(self, delay):
        self.delay = delay

    def set_ccw(self, ccw):
        self.ccw = ccw

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
        for i in range(0, cycles):
            if self.ccw:
                self.ccw_cycle()
            else:
                self.cw_cycle()

class KalCamera:

    def __init__(self, picFile="pic#0#.jpg",vidFile = "vid#0#.h264"):
        self.picFile = picFile
        self.vidFile = vidFile

    def pic(self, filename=None):
        camera = PiCamera()
        camera.resolution = (1024,768)
        camera.start_preview(alpha=200)
        sleep(1)
        if filename != None:
            camera.capture("Pictures/" + filename + ".jpg")
        else:
            camera.capture("Pictures/" + self.picFile)
            tmp = self.picFile.split('#')
            tmp[1] = str(int(tmp[1]) + 1)
            self.picFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.stop_preview()
        camera.close()
    
    def vid(self, dur, filename=None):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24

        camera.start_preview(alpha=200)
        camera.preview_fullscreen = False
        camera.preview.window = (300, 200, 1920, 1080)
        if filename != None:
            camera.start_recording("Videos/" + filename + ".h264")
        else:
            camera.start_recording("Videos/" + self.vidFile)
            tmp = self.vidFile.split('#')
            tmp[1] = str(int(tmp[1]) + 1)
            self.vidFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.wait_recording(dur)
        camera.stop_recording()
        camera.stop_preview()
        camera.close()

class KalLED:

    def __init__(self, pins, dcs=(0, 0, 0)):
        self.pins = pins
        self.rdc = dcs[0]
        self.gdc = dcs[1]
        self.bdc = dcs[2]
        self.r = GPIO.PWM(pins[0], 120)
        self.g = GPIO.PWM(pins[1], 120)
        self.b = GPIO.PWM(pins[2], 120)

    def start(self):
        self.r.start(self.rdc)
        self.g.start(self.gdc)
        self.b.start(self.bdc)

    def stop(self):
        self.r.stop()
        self.g.stop()
        self.b.stop()

    def set_dc(self, rdc_new, gdc_new, bdc_new):
        self.rdc = rdc_new
        self.gdc = gdc_new
        self.bdc = bdc_new
        self.r.ChangeDutyCycle(rdc_new)
        self.g.ChangeDutyCycle(gdc_new)
        self.b.ChangeDutyCycle(bdc_new)
