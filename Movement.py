import serial
import time
from Sensors import SensorsController


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
        self.ser.write(str(int(a1)) + "q" + str(int(a2)) + "w" + str(int(b1)) + "e" + str(int(b2)) + "r" + str(
            int(c1)) + "t" + str(int(c2)) + "y" + str(int(d1)) + "u" + str(int(d2)) + "i")


class MovementAlgorithms(AppliedMovement, SensorsController):
    just_move_value = 511
    outside_corner_movement_time = 0.15
    pre_cliff_time = 0.1

    def __init__(self):
        super(AppliedMovement, self).__init__()
        super(SensorsController, self).__init__()

    def do_front_align(self):
        while True:
            print("Doing front align")
            d1, d2 = self.get_front_l_dist(), self.get_front_r_dist()
            err = self.get_align_circle_err(d1=d1, d2=d2)
            print("                        " + str(d1) + " " + str(d2) + " " + str(err))
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_clockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_counterclockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                err = self.get_align_progressive_err(mid)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_straight(err)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_back(err)
                else:
                    self.stop_move()
                    return

    def do_left_align(self):
        while True:
            print("Doing left align")
            d1, d2 = self.get_left_f_dist(), self.get_left_b_dist()
            err = self.get_align_circle_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                err = self.get_align_progressive_err(mid)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_left(err)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_right(err)
                else:
                    self.stop_move()
                    return

    def do_back_align(self):
        while True:
            print("Doing back align")
            d1, d2 = self.get_back_l_dist(), self.get_back_r_dist()
            err = self.get_align_circle_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                err = self.get_align_progressive_err(mid)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_back(err)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_straight(err)
                else:
                    self.stop_move()
                    return

    def do_right_align(self):
        while True:
            print("Doing right align")
            d1, d2 = self.get_right_b_dist(), self.get_right_f_dist()
            err = self.get_align_circle_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                err = self.get_align_progressive_err(mid)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_right(err)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_left(err)
                else:
                    self.stop_move()
                    return

    def leave_front_l_around_corner(self):
        print("leave_front_l_around_corner")
        time.sleep(self.pre_cliff_time)
        l_f_been, l_b_been = self.is_wall_left_f(), self.is_wall_left_b()
        print("been:", l_f_been, l_b_been)
        while l_f_been == self.is_wall_left_f() and l_b_been == self.is_wall_left_b():
            print(self.is_wall_left_f(), "and", self.is_wall_left_b())
            self.move_straight(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_front_r_around_corner(self):
        print("leave_front_r_around_corner")
        time.sleep(self.pre_cliff_time)
        r_f_been, r_b_been = self.is_wall_right_f(), self.is_wall_right_b()
        print("been:", r_f_been, r_b_been)
        while r_f_been == self.is_wall_right_f() and r_b_been == self.is_wall_right_b():
            print(self.is_wall_right_f(), "and", self.is_wall_right_b())
            self.move_straight(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_right_f_around_corner(self):
        print("leave_right_f_around_corner")
        time.sleep(self.pre_cliff_time)
        f_r_been, f_l_been = self.is_wall_front_r(), self.is_wall_front_l()
        print("been:", f_r_been, f_l_been)
        while f_r_been == self.is_wall_front_r() and f_l_been == self.is_wall_front_l():
            print(self.is_wall_front_r(), "and", self.is_wall_front_l())
            self.move_right(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_right_b_around_corner(self):
        print("leave_right_b_around_corner")
        time.sleep(self.pre_cliff_time)
        b_l_been, b_r_been = self.is_wall_back_l(), self.is_wall_back_r()
        print("been:", b_l_been, b_r_been)
        while b_l_been == self.is_wall_back_l() and b_r_been == self.is_wall_back_r():
            print(b_l_been == self.is_wall_back_l(), "and", self.is_wall_back_r())
            self.move_right(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_back_r_around_corner(self):
        print("leave_back_r_around_corner")
        time.sleep(self.pre_cliff_time)
        r_f_been, r_b_been = self.is_wall_right_f(), self.is_wall_right_b()
        print("been:", r_f_been, r_b_been)
        while r_f_been == self.is_wall_right_f() and r_b_been == self.is_wall_right_b():
            print(self.is_wall_right_f(), "and", self.is_wall_right_b())
            self.move_back(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_back_l_around_corner(self):
        print("leave_back_l_around_corner")
        time.sleep(self.pre_cliff_time)
        l_b_been, l_f_been = self.is_wall_left_b(), self.is_wall_left_f()
        print("been:", l_b_been, l_f_been)
        while l_b_been == self.is_wall_left_b() and l_f_been == self.is_wall_left_f():
            print(self.is_wall_left_b(), "and", self.is_wall_left_f())
            self.move_back(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_left_b_around_corner(self):
        print("leave_left_b_around_corner")
        time.sleep(self.pre_cliff_time)
        b_r_been, b_l_been = self.is_wall_back_r(), self.is_wall_back_l()
        print("been:", b_r_been, b_l_been)
        while b_r_been == self.is_wall_back_r() and b_l_been == self.is_wall_back_l():
            print(self.is_wall_back_r(), "and", self.is_wall_back_l())
            self.move_left(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_left_f_around_corner(self):
        print("leave_left_f_around_corner")
        time.sleep(self.pre_cliff_time)
        f_r_been, f_l_been = self.is_wall_front_r(), self.is_wall_front_l()
        print("been:", f_r_been, f_l_been)
        while f_r_been == self.is_wall_front_r() and f_l_been == self.is_wall_front_l():
            print(self.is_wall_front_r(), "and", self.is_wall_front_l())
            self.move_right(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()
