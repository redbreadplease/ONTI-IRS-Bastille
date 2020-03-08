#!/usr/bin/env python
import serial
import sys
import os

sys.path.insert(0, os.pardir)


class OpticalFlowController:
    def __init__(self):
        ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
        # ser = serial.Serial ("/dev/ttyS0", 9600)

    def get_bias(self):
        x = ""
        a = ""
        while a != "x":
            a = ser.read()
            if (a != "x"):
                x = x + a
        y = ""
        a = ""
        while a != "y":
            a = ser.read()
            if (a != "y"):
                y = y + a
        print("x" + str(x))
        print("y" + str(y))
        err = (2650 - int(y)) * 1.2
        if (err > 400):
            err = 400
        if (err < 0):
            err = 0
        upr = "0q" + str(err) + "w0e" + str(err) + "r0t" + str(err) + "y0u" + str(err) + "i"
        ser.write(upr)
