#!/usr/bin/env python
import time

from MainController import RobotController

right_dist_drive, dist_now = 600, 0
inverse_moving = False

robot_controller = RobotController()

try:
    robot_controller.move_straight(255)
    time.sleep(0.1)

    if robot_controller.get_bias_x_y()[0] < 0:
        inverse_moving = True

    print("inverse: " + str(inverse_moving))

    while True:
        dist_now += robot_controller.get_bias_x_y()[1]

        print("                                                               dist: " + str(dist_now))
        print("Row optical flow values: " + str(robot_controller.get_optical_flow_row_values()))

        if dist_now > right_dist_drive:
            if not inverse_moving:
                robot_controller.move_straight(255)
            else:
                robot_controller.move_back(255)
            print("Moving minus")
        elif dist_now < -right_dist_drive:
            if not inverse_moving:
                robot_controller.move_back(255)
            else:
                robot_controller.move_straight(255)
            print("Moving plus")
finally:
    robot_controller.stop_move()
