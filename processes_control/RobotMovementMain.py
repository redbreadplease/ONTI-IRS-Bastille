from RobotController import RobotController
import time

valera = RobotController()

try:
    direction = 0

    while True:
        if direction == 0:
            print "D0"
            if valera.is_right_f_diff_with_prev_means_cliff() and valera.is_align_finished:
                valera.go_around_outside_corner_f_r()
                direction = 3
            elif valera.is_wall_front():
                direction = 1
            elif valera.is_align_right_necessary():
                valera.do_right_align()
            else:
                valera.move_straight(255)
        elif direction == 1:
            print "D1"
            if valera.is_front_l_diff_with_prev_means_cliff() and valera.is_align_finished:
                valera.go_around_outside_corner_l_f()
                direction = 0
            elif valera.is_wall_left():
                direction = 2
            elif valera.is_align_front_necessary():
                valera.do_front_align()
            else:
                valera.move_left(255)
        elif direction == 2:
            print "D2"
            if valera.is_left_b_diff_with_prev_means_cliff() and valera.is_align_finished:
                valera.go_around_outside_corner_b_l()
                direction = 1
            elif valera.is_wall_back():
                direction = 3
            elif valera.is_align_left_necessary():
                valera.do_left_align()
            else:
                valera.move_back(255)
        elif direction == 3:
            print "D3"
            if valera.is_back_r_diff_with_prev_means_cliff() and valera.is_align_finished:
                valera.go_around_outside_corner_r_b()
                direction = 2
            elif valera.is_wall_right():
                direction = 0
            elif valera.is_align_back_necessary():
                valera.do_back_align()
            else:
                valera.move_right(255)
except KeyboardInterrupt:
    valera.stop_move()
    valera.sensors_controller.shut_down()
