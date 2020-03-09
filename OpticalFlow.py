#!/usr/bin/env python
from math import sqrt

import serial


class OpticalFlowController:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
        self.prev_x, self.prev_y = self.get_values_now()

    def get_values_now(self):
        x_now, y_now = "", ""
        while True:
            symbol = self.ser.read()
            if symbol != "x":
                x_now += symbol
            else:
                x_now = int(x_now)
                break
        while True:
            symbol = self.ser.read()
            if symbol != "y":
                y_now += symbol
            else:
                y_now = int(y_now)
                break
        return x_now, y_now

    def get_bias_x_y(self):
        x_now, y_now = self.get_values_now()
        return self.prev_x - x_now, self.prev_y - y_now

    def get_bias_distance(self):
        bias_x, bias_y = self.get_bias_x_y()
        return sqrt(bias_x ** 2 + bias_y ** 2)

    def reset(self):
        self.prev_x, self.prev_y = self.get_values_now()

    def get_cells_driven_since_last_time_amount(self):
        pass