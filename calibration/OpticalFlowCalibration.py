#!/usr/bin/env python
import serial
from RobotController import RobotController

dist_drive = 100

robot_controller = RobotController()

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)

prev_x, prev_y = 0, 0
dist = 0

while True:
    # ser = serial.Serial ("/dev/ttyS0", 9600)
    x = ""
    a = ""
    while a != "x":
        a = ser.read()
        if a != "x":
            x = x + a

    y = ""
    a = ""
    while a != "y":
        a = ser.read()
        if a != "y":
            y = y + a

    print("x" + str(x) + " y" + str(y))
    if prev_x and prev_y:
        dist += (prev_x - x)
    prev_x, prev_y = x, y

    if dist < dist_drive:
        robot_controller.move_straight(255)
    elif -dist > dist_drive:
        robot_controller.move_back(255)
