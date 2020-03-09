#!/usr/bin/env python
import time

from MainController import RobotController

right_dist_drive = 150

robot_controller = RobotController()

dist_now = 0

inverse_moving, moving_plus = False, True

try:
    robot_controller.move_straight(255)
    time.sleep(0.1)
    if robot_controller.get_bias_x_y()[0] < 0:
        inverse_moving = True
    while True:
        dist_now += robot_controller.get_bias_x_y()[0]

        if dist_now > right_dist_drive:
            moving_plus = False
        elif dist_now < -right_dist_drive:
            moving_plus = True

        if not inverse_moving:
            if moving_plus:
                robot_controller.move_straight(255)
            else:
                robot_controller.move_back(255)
        else:
            if not moving_plus:
                robot_controller.move_straight(255)
            else:
                robot_controller.move_back(255)

finally:
    robot_controller.stop_move()
