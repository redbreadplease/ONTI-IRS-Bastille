#!/usr/bin/env python
from math import sqrt

import serial


class OpticalFlowChecker(object):
    def __init__(self):
        self.prev_optical_flow_x, self.prev_optical_flow_y = None, None

    @staticmethod
    def get_optical_flow_row_values():
        ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
        x_now, y_now = "", ""
        while True:
            symbol = ser.read()
            if symbol != "x":
                x_now += symbol
            else:
                x_now = int(x_now)
                break
        while True:
            symbol = ser.read()
            if symbol != "y":
                y_now += symbol
            else:
                y_now = int(y_now)
                break
        return x_now, y_now

    def get_bias_x_y(self):
        if self.prev_optical_flow_x is None and self.prev_optical_flow_y is None:
            self.prev_optical_flow_x, self.prev_optical_flow_y = self.get_optical_flow_row_values()

        x_now, y_now = self.get_optical_flow_row_values()
        bias_x, bias_y = self.prev_optical_flow_x - x_now, self.prev_optical_flow_y - y_now

        self.prev_optical_flow_x, self.prev_optical_flow_y = x_now, y_now

        return bias_x, bias_y

    def get_bias_distance(self):
        bias_x, bias_y = self.get_bias_x_y()
        return sqrt(bias_x ** 2 + bias_y ** 2)

    def reset(self):
        self.prev_optical_flow_x, self.prev_optical_flow_y = self.get_optical_flow_row_values()

    def get_cells_driven_since_last_time_amount(self):
        pass


class OpticalFlowController(OpticalFlowChecker):
    def __init__(self):
        super(OpticalFlowChecker, self).__init__()

    def get_front_bias(self):
        return self.get_bias_x_y()[1]

    def get_left_bias(self):
        return self.get_bias_x_y()[0]

    def get_back_bias(self):
        return -self.get_bias_x_y()[1]

    def get_right_bias(self):
        return -self.get_bias_x_y()[0]
