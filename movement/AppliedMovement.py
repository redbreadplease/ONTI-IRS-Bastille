import serial
import sys
import os

sys.path.insert(0, os.pardir)


class AppliedMovement:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def move_clockwise(self, val):
        self.signal_to_move(0, 0, val, val, 0, val, 0, val)

    def move_counterclockwise(self, val):
        self.signal_to_move(val, val, 0, 0, val, 0, val, 0)

    def move_back(self, val):
        self.signal_to_move(val, 0, val, 0, val, 0, val, 0)

    def move_right(self, val):
        self.signal_to_move(0, 0, val, 0, val, val, 0, val)

    def move_straight(self, val):
        self.signal_to_move(0, val, 0, val, 0, val, 0, val)

    def move_left(self, val):
        self.signal_to_move(val, val, 0, val, 0, 0, val, 0)

    def stop_move(self):
        self.signal_to_move(0, 0, 0, 0, 0, 0, 0, 0)

    def signal_to_move(self, a1, a2, b1, b2, c1, c2, d1, d2):
        self.ser.write(str(int(a1)) + "q" + str(int(a2)) + "w" + str(int(b1)) + "e" + str(int(b2)) + "r" + str(
            int(c1)) + "t" + str(int(c2)) + "y" + str(int(d1)) + "u" + str(int(d2)) + "i")
