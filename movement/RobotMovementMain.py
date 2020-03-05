import time

from RobotController import RobotController

valera = RobotController()

try:
    direction = 2

    while True:
        f = open('fuck.txt', 'r')
        context = f.read()
        f.close()
        f = open('fuck.txt', 'w')
        f.write(context)
        f.write(str(valera.sensors_controller.tof_left_b.get_distance()) + " " + str(
            valera.sensors_controller.tof_left_f.get_distance()) + "\n")
        f.close()
        if direction == 0:
            print "D0"
            if valera.is_right_cliff_started() or not valera.is_wall_right_f():
                print "1"
                valera.go_around_outside_corner_f_r()
                direction = 3
            elif valera.is_wall_front():
                print "2"
                direction = 1
            elif valera.is_align_right_necessary():
                print "3"
                valera.do_right_align()
                time.sleep(0.05)
                valera.move_straight(255)
                time.sleep(0.05)
            else:
                print "4"
                valera.move_straight(255)

        elif direction == 1:
            print "D1"
            print str(abs((valera.sensors_controller.prev_front_l_value - valera.sensors_controller.get_front_l_dist())
                          - (valera.sensors_controller.prev_front_r_value
                             - valera.sensors_controller.get_front_r_dist())))
            if valera.is_front_cliff_started() or not valera.is_wall_front_r():
                valera.go_around_outside_corner_l_f()
                direction = 0
            elif valera.is_wall_left():
                direction = 2
            elif valera.is_align_front_necessary():
                valera.do_front_align()
                time.sleep(0.05)
                valera.move_left(255)
                time.sleep(0.05)
            else:
                valera.move_left(255)

        elif direction == 2:
            print "D2"
            if valera.is_left_cliff_started() or not valera.is_wall_left_b():
                valera.go_around_outside_corner_b_l()
                direction = 1
            elif valera.is_wall_back():
                direction = 3
            elif valera.is_align_left_necessary():
                valera.do_left_align()
                time.sleep(0.05)
                valera.move_back(255)
                time.sleep(0.05)
            else:
                valera.move_back(255)
        elif direction == 3:
            print "D3"
            if valera.is_back_cliff_started() or not valera.is_wall_back_l():
                valera.go_around_outside_corner_r_b()
                direction = 2
            elif valera.is_wall_right():
                direction = 0
            elif valera.is_align_back_necessary():
                valera.do_back_align()
                time.sleep(0.05)
                valera.move_right(255)
                time.sleep(0.05)
            else:
                valera.move_right(255)
except KeyboardInterrupt:
    valera.stop_move()
    valera.sensors_controller.shut_down()
