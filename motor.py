import RPi.GPIO as gpio
from time import sleep

class Motor:

    def __init__(self, pins, delay):
        self.pins = pins
        self.delay = delay
        self.ccw_steps_logic = [[1, 1, 0, 0],
                                [1, 0, 0, 1],
                                [0, 0, 1, 1],
                                [0, 1, 1, 0]]
        self.cw_steps_logic = [[1, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 1, 1],
                               [1, 0, 0, 1]]

    def read_states(self, states):
        gpio.output(self.pins, states)

    def ccw_cycle(self, cycles=1):
        for i in range(0, cycles):
            for j in range(len(self.ccw_steps_logic)):
                self.read_states(self.ccw_steps_logic[j])
                sleep(self.delay)
