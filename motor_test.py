import RPi.GPIO as gpio
from motor import Motor

pins = [22, 17, 23, 27] #[a1, b1, a2, b2]
delay = 0.01

motor = Motor(pins, delay)

gpio.setmode(gpio.BCM)
gpio.setup(motor.pins, gpio.OUT)

motor.ccw_cycle(100)

gpio.cleanup(motor.pins)
