import serial
import time
from Sensors import SensorsController


class AppliedMovement(object):
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyS0", 9600, timeout=5)
        '''self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )'''

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
    outside_corner_movement_time = 0.2

    def __init__(self):
        super(AppliedMovement, self).__init__()
        super(SensorsController, self).__init__()

    def do_front_align(self):
        while True:
            d1, d2 = self.get_front_l_dist(), self.get_front_r_dist()
            err = self.get_align_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_clockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_counterclockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_straight(mid - self.right_align_distance)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_back(mid - self.right_align_distance)
                else:
                    return

    def do_left_align(self):
        while True:
            d1, d2 = self.get_left_f_dist(), self.get_left_b_dist()
            err = self.get_align_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_left(mid - self.right_align_distance)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_right(mid - self.right_align_distance)
                else:
                    return

    def do_back_align(self):
        while True:
            d1, d2 = self.get_back_l_dist(), self.get_back_r_dist()
            err = self.get_align_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_back(mid - self.right_align_distance)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_straight(mid - self.right_align_distance)
                else:
                    return

    def do_right_align(self):
        while True:
            d1, d2 = self.get_right_b_dist(), self.get_right_f_dist()
            err = self.get_align_err(d1=d1, d2=d2)
            if self.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.get_mid_value(d1, d2)
                if self.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_right(mid - self.right_align_distance)
                elif self.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_left(mid - self.right_align_distance)
                else:
                    return

    def leave_front_l_around_corner(self):
        while self.is_wall_front_r() or self.is_wall_front_l():
            self.move_left(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_front_r_around_corner(self):
        while self.is_wall_front_r() or self.is_wall_front_l():
            self.move_right(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_right_f_around_corner(self):
        while self.is_wall_right_f() or self.is_wall_right_b():
            self.move_straight(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_right_b_around_corner(self):
        while self.is_wall_right_f() or self.is_wall_right_b():
            self.move_back(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_back_r_around_corner(self):
        while self.is_wall_back_l() or self.is_wall_back_r():
            self.move_right(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_back_l_around_corner(self):
        while self.is_wall_back_l() or self.is_wall_back_r():
            self.move_left(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_left_b_around_corner(self):
        while self.is_wall_left_b() or self.is_wall_left_f():
            self.move_back(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()

    def leave_left_f_around_corner(self):
        while self.is_wall_left_b() or self.is_wall_left_f():
            self.move_straight(self.just_move_value)
        time.sleep(self.outside_corner_movement_time)
        self.stop_move()
