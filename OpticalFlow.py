#!/usr/bin/env python
from math import sqrt

import serial


class OpticalFlowChecker(object):

    def __init__(self):
        # self.prev_optical_flow_x, self.prev_optical_flow_y = self.get_optical_flow_row_values()
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

            print("EBANOE OPTICALFLOW Y")

            if symbol == "y":
                continue

            if symbol != "x":
                x_now += symbol
            else:
                x_now = int(x_now)
                break
        while True:
            symbol = ser.read()

            print("EBANOE OPTICALFLOW X")

            if not symbol:
                break
            if symbol != "y":
                y_now += symbol
            else:
                y_now = int(y_now)
                break
        return x_now, y_now

    def get_bias_x_y(self):
        x_now, y_now = self.get_optical_flow_row_values()
        bias_x, bias_y = self.prev_optical_flow_x - x_now, self.prev_optical_flow_y - y_now

        self.prev_optical_flow_x, self.prev_optical_flow_y = x_now, y_now

        return bias_x, bias_y

    def get_bias_distance(self):
        bias_x, bias_y = self.get_bias_x_y()
        return sqrt(bias_x ** 2 + bias_y ** 2)

    def reset(self):
        self.prev_optical_flow_x, self.prev_optical_flow_y = self.get_optical_flow_row_values()


class OpticalFlowController(OpticalFlowChecker):
    optical_flow_cell_size = 1300.

    def __init__(self):
        super(OpticalFlowChecker, self).__init__()

    def get_front_bias(self):
        return -self.get_bias_x_y()[1]

    def get_left_bias(self):
        return self.get_bias_x_y()[0]

    def get_back_bias(self):
        return self.get_bias_x_y()[1]

    def get_right_bias(self):
        return -self.get_bias_x_y()[0]

    def get_cells_driven_since_last_time_amount(self):
        print("Cells\'ve driven: ")
        try:
            return int(input())
        except ValueError:
            return int(input())
        # return int(float(self.get_bias_distance()) / (self.optical_flow_cell_size * 0.9))
