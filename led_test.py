import RPi.GPIO as GPIO
from time import sleep
a=6
b=13
c=19
GPIO.setmode(GPIO.BCM)

GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(c, GPIO.OUT)

#for i in range(10):
    #GPIO.output(6, 1)
    #sleep(0.5)
    #GPIO.output(6, 0)
    #sleep(0.5)

#GPIO.cleanup(6)

r = GPIO.PWM(a,100)
g = GPIO.PWM(b,100)
b = GPIO.PWM(c,100)
r.start(0)
g.start(0)
b.start(0)
try:
    while 1:
        for dc in range(0,101,5):
            r.ChangeDutyCycle(dc)
            g.ChangeDutyCycle(dc)
            b.ChangeDutyCycle(dc)
            sleep(0.01)
        for dc in range(100,-1,-5):
            r.ChangeDutyCycle(dc)
            g.ChangeDutyCycle(dc)
            b.ChangeDutyCycle(dc)
            sleep(0.01)
except KeyboardInterrupt:
    pass

r.stop()
g.stop()
b.stop()
GPIO.cleanup()
