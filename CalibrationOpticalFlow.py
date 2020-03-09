#!/usr/bin/env python
import serial

from MainController import RobotController

dist_drive = 150

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

try:
    robot_controller.move_straight(255)

    while True:
        x, y = "", ""
        while True:
            symbol = ser.read()
            if symbol != "x":
                x = x + symbol
            else:
                x = int(x)
                break
        while True:
            symbol = ser.read()
            if symbol != "y":
                y = y + symbol
            else:
                y = int(y)
                break
        print("x" + str(x) + " y" + str(y))

        if prev_x and prev_y:
            dist += (prev_y - y)
        prev_x, prev_y = x, y

        print("dist: " + str(dist))

        if dist < dist_drive:
            robot_controller.move_straight(255)
        elif -dist > dist_drive:
            robot_controller.move_back(255)
finally:
    robot_controller.stop_move()
