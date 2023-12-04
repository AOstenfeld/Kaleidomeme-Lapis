import RPi.GPIO as gpio
from mods import Motor

pins = [22, 17, 23, 27] #[a1, b1, a2, b2]
delay = 0.02

motor = Motor(pins, delay)

motor.cycle(int(1/delay))

motor.clean()
