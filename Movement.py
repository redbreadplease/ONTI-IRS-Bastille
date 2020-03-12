from Sensors import SensorsController
import serial
import time


class AppliedMovement(object):
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyS0", 9600, timeout=5)

    def move_clockwise(self, val):
        self.signal_to_move(0, 0, val, 0, val, val, 0, val)

    def move_counterclockwise(self, val):
        self.signal_to_move(val, val, 0, val, 0, 0, val, 0)

    def move_back(self, val):
        self.signal_to_move(val, 0, val, 0, val, 0, val, 0)

    def move_right(self, val):
        self.signal_to_move(val, val, 0, 0, val, val, 0, 0)

    def move_straight(self, val):
        self.signal_to_move(0, val, 0, val, 0, val, 0, val)

    def move_left(self, val):
        self.signal_to_move(0, 0, val, val, 0, 0, val, val)

    def stop_move(self):
        self.signal_to_move(0, 0, 0, 0, 0, 0, 0, 0)

    def signal_to_move(self, a1, a2, b1, b2, c1, c2, d1, d2):
        self.ser.write(str(int(a1)) + "q" + str(int(a2)) + "w" + str(int(b1)) + "e" + str(int(b2)) + "r" +
                       str(int(c1)) + "t" + str(int(c2)) + "y" + str(int(d1)) + "u" + str(int(d2)) + "i")


class MovementAlgorithms(AppliedMovement, SensorsController):
    just_move_value = 255
    outside_corner_movement_time = 0.1
    pre_cliff_time = 0.5

    def __init__(self):
        super(AppliedMovement, self).__init__()
        super(SensorsController, self).__init__()

    def do_align(self, get_first_dist, get_second_dist, move_to_wall, move_from_wall):
        while True:
            d1, d2 = get_first_dist(), get_second_dist()
            print("d1: " + str(d1) + "  d2: " + str(d2))
            circle_err = self.get_align_circle_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(circle_err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(circle_err)
            else:
                mid_dist = self.get_mid_value(d1, d2)
                progressive_err = self.get_align_progressive_err(mid_dist)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid_dist):
                    move_to_wall(progressive_err)
                elif self.does_side_sensors_difference_means_go_from_wall(mid_dist):
                    move_from_wall(progressive_err)
                else:
                    self.stop_move()
                    return

    def do_front_align(self):
        self.do_align(self.get_front_l_dist, self.get_front_r_dist, self.move_straight, self.move_back)

    def do_left_align(self):
        self.do_align(self.get_left_f_dist, self.get_left_b_dist, self.move_left, self.move_right)

    def do_back_align(self):
        self.do_align(self.get_back_l_dist, self.get_back_r_dist, self.move_back, self.move_straight)

    def do_right_align(self):
        self.do_align(self.get_right_b_dist, self.get_right_f_dist, self.move_right, self.move_left)

    def leave_around_corner(self, is_first_wall, is_second_wall, do_align, move):
        time.sleep(self.pre_cliff_time)
        first_was, second_was, i = is_first_wall(), is_second_wall(), 0
        while first_was == is_first_wall() and second_was == is_second_wall():
            if i > 100:
                do_align()
                i = 0
            move(self.just_move_value)
            i += 1
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_front_l_around_corner(self):
        print("leave_front_l_around_corner")
        self.leave_around_corner(self.is_wall_left_f, self.is_wall_left_b, self.do_left_align, self.move_straight)

    def leave_front_r_around_corner(self):
        print("leave_front_r_around_corner")
        self.leave_around_corner(self.is_wall_right_f, self.is_wall_right_b, self.do_right_align, self.move_straight)

    def leave_right_f_around_corner(self):
        print("leave_right_f_around_corner")
        self.leave_around_corner(self.is_wall_front_r, self.is_wall_front_l, self.do_front_align, self.move_right)

    def leave_right_b_around_corner(self):
        print("leave_right_b_around_corner")
        self.leave_around_corner(self.is_wall_back_l, self.is_wall_back_r, self.do_back_align, self.move_right)

    def leave_back_r_around_corner(self):
        print("leave_back_r_around_corner")
        self.leave_around_corner(self.is_wall_right_f, self.is_wall_right_b, self.do_right_align, self.move_back)

    def leave_back_l_around_corner(self):
        print("leave_back_l_around_corner")
        self.leave_around_corner(self.is_wall_left_b, self.is_wall_left_f, self.do_left_align, self.move_back)

    def leave_left_b_around_corner(self):
        print("leave_left_b_around_corner")
        self.leave_around_corner(self.is_wall_back_r, self.is_wall_back_l, self.do_back_align, self.move_left)

    def leave_left_f_around_corner(self):
        print("leave_left_f_around_corner")
        self.leave_around_corner(self.is_wall_front_r, self.is_wall_front_l, self.do_front_align, self.move_right)
