import time

from SensorsController import SensorsController
from RobotLogic import RobotLogic


class RobotController:
    P_koef = 3.0
    right_distance = 110
    min_react_value = 10
    wall_dist_deviation = 20
    min_hole_distance = 350
    min_cliff_value = 50
    corner_step = 0.2

    def __init__(self):
        self.sensors_controller = SensorsController()
        self.robot_logic = RobotLogic()

    def do_front_align(self):
        d1, d2 = self.sensors_controller.get_front_l_dist(), self.sensors_controller.get_front_r_dist()
        err = self.robot_logic.get_align_err(d1=d1, d2=d2)
        if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
            self.move_clockwise(err)
        elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
            self.move_counterclockwise(err)
        else:
            mid = self.robot_logic.get_mid_value(d1, d2)
            if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                self.move_straight(mid - self.right_distance)
            elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                self.move_back(mid - self.right_distance)

    def do_left_align(self):
        d1, d2 = self.sensors_controller.get_left_f_dist(), self.sensors_controller.get_left_b_dist()
        err = self.robot_logic.get_align_err(d1=d1, d2=d2)
        if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
            self.move_counterclockwise(err)
        elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
            self.move_clockwise(err)
        else:
            mid = self.robot_logic.get_mid_value(d1, d2)
            if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                self.move_left(mid - self.right_distance)
            elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                self.move_right(mid - self.right_distance)

    def do_back_align(self):
        d1, d2 = self.sensors_controller.get_back_l_dist(), self.sensors_controller.get_back_r_dist()
        err = self.robot_logic.get_align_err(d1=d1, d2=d2)
        if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
            self.move_counterclockwise(err)
        elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
            self.move_clockwise(err)
        else:
            mid = self.robot_logic.get_mid_value(d1, d2)
            if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                self.move_back(mid - self.right_distance)
            elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                self.move_straight(mid - self.right_distance)

    def do_right_align(self):
        d1, d2 = self.sensors_controller.get_right_b_dist(), self.sensors_controller.get_right_f_dist()
        err = self.robot_logic.get_align_err(d1=d1, d2=d2)
        if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
            self.move_counterclockwise(err)
        elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
            self.move_clockwise(err)
        else:
            mid = self.robot_logic.get_mid_value(d1, d2)
            if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                self.move_right(mid - self.right_distance)
            elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                self.move_left(mid - self.right_distance)

    def move_clockwise(self, value):
        self.sensors_controller.signal_to_move(value, value, 0, value, 0, value, 0, 0)

    def move_counterclockwise(self, value):
        self.sensors_controller.signal_to_move(0, 0, value, 0, value, 0, value, value)

    def move_back(self, val):
        self.sensors_controller.signal_to_move(0, val, val, 0, val, val, 0, 0)

    def move_right(self, val):
        self.sensors_controller.signal_to_move(val, val, 0, 0, val, 0, val, 0)

    def move_straight(self, val):
        self.sensors_controller.signal_to_move(val, 0, 0, val, 0, 0, val, val)

    def move_left(self, val):
        self.sensors_controller.signal_to_move(0, 0, val, val, 0, val, 0, val)

    def is_wall_front(self):
        return (self.sensors_controller.get_front_r_dist() + self.sensors_controller.get_front_l_dist()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_left(self):
        return (self.sensors_controller.get_left_b_dist() + self.sensors_controller.get_left_f_dist()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_back(self):
        return (self.sensors_controller.get_back_l_dist() + self.sensors_controller.get_back_r_dist()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_right(self):
        return (self.sensors_controller.get_right_b_dist() + self.sensors_controller.get_right_f_dist()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def stop_move(self):
        self.sensors_controller.signal_to_move(0, 0, 0, 0, 0, 0, 0, 0)

    def is_align_front_necessary(self):
        d1, d2 = self.sensors_controller.get_front_l_dist(), self.sensors_controller.get_front_r_dist()
        if abs(d1 - d2) > self.min_react_value or abs(
                (d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_left_necessary(self):
        d1, d2 = self.sensors_controller.get_left_b_dist(), self.sensors_controller.get_left_f_dist()
        if abs(d1 - d2) > self.min_react_value or abs(
                (d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_back_necessary(self):
        d1, d2 = self.sensors_controller.get_back_l_dist(), self.sensors_controller.get_back_r_dist()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_right_necessary(self):
        d1, d2 = self.sensors_controller.get_right_f_dist(), self.sensors_controller.get_right_b_dist()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_wall_right_b(self):
        return self.sensors_controller.get_right_b_dist() < self.min_hole_distance

    def is_wall_right_f(self):
        return self.sensors_controller.get_right_f_dist() < self.min_hole_distance

    def is_wall_front_r(self):
        return self.sensors_controller.get_front_r_dist() < self.min_hole_distance

    def is_wall_front_l(self):
        return self.sensors_controller.get_front_l_dist() < self.min_hole_distance

    def is_wall_left_f(self):
        return self.sensors_controller.get_left_f_dist() < self.min_hole_distance

    def is_wall_left_b(self):
        return self.sensors_controller.get_left_b_dist() < self.min_hole_distance

    def is_wall_back_l(self):
        return self.sensors_controller.get_back_l_dist() < self.min_hole_distance

    def is_wall_back_r(self):
        return self.sensors_controller.get_back_r_dist() < self.min_hole_distance

    def is_front_l_diff_with_prev_means_cliff(self):
        if self.sensors_controller.tof_front_l.get_distance() - self.sensors_controller.prev_front_l_value > self.min_cliff_value:
            return self.sensors_controller.get_front_l_dist() - self.sensors_controller.prev_front_l_value > self.min_cliff_value

    def is_left_b_diff_with_prev_means_cliff(self):
        if self.sensors_controller.tof_left_b.get_distance() - self.sensors_controller.prev_left_b_value > self.min_cliff_value:
            return self.sensors_controller.get_left_b_dist() - self.sensors_controller.prev_left_b_value > self.min_cliff_value

    def is_back_r_diff_with_prev_means_cliff(self):
        if self.sensors_controller.tof_back_r.get_distance() - self.sensors_controller.prev_back_r_value > self.min_cliff_value:
            return self.sensors_controller.get_back_r_dist() - self.sensors_controller.prev_back_r_value > self.min_cliff_value

    def is_right_f_diff_with_prev_means_cliff(self):
        if self.sensors_controller.tof_right_f.get_distance() - self.sensors_controller.prev_right_f_value > self.min_cliff_value:
            return self.sensors_controller.get_right_f_dist() - self.sensors_controller.prev_right_f_value > self.min_cliff_value

    def is_front_diff_with_prev_means_cliff(self):
        if self.sensors_controller.tof_front_l.get_distance() - self.sensors_controller.prev_front_l_value > self.min_cliff_value:
            return self.sensors_controller.get_front_l_dist() - self.sensors_controller.prev_front_l_value > self.min_cliff_value

    def go_around_outside_corner_f_r(self):
        while self.is_wall_right_b():
            self.move_straight(255)
        time.sleep(self.corner_step)
        while not self.is_wall_back_r():
            self.move_right(255)
        while not self.is_wall_back_l():
            self.move_right(255)
        time.sleep(self.corner_step)

    def go_around_outside_corner_l_s(self):
        while self.is_wall_front_r():
            self.move_left(255)
        time.sleep(self.corner_step)
        while not self.is_wall_right_f():
            self.move_straight(255)
        while not self.is_wall_right_b():
            self.move_straight(255)
        time.sleep(self.corner_step)

    def go_around_outside_corner_b_l(self):
        while self.is_wall_left_f():
            self.move_back(255)
        time.sleep(self.corner_step)
        while not self.is_wall_front_l():
            self.move_left(255)
        while not self.is_wall_front_r():
            self.move_left(255)
        time.sleep(self.corner_step)

    def go_around_outside_corner_r_b(self):
        while self.is_wall_back_l():
            self.move_right(255)
        time.sleep(self.corner_step)
        while not self.is_wall_left_b():
            self.move_back(255)
        while not self.is_wall_left_f():
            self.move_back(255)
        time.sleep(self.corner_step)

    def go_around_outside_corner_s_l(self):
        while self.is_wall_left_b():
            self.move_straight(255)
        time.sleep(self.corner_step)
        while not self.is_wall_back_l():
            self.move_left(255)
        while not self.is_wall_back_r():
            self.move_left(255)
        time.sleep(self.corner_step)

    def go_around_outside_corner_l_f(self):
        while self.is_wall_front_r():
            self.move_left(255)
        time.sleep(self.corner_step)
        while not self.is_wall_left_f():
            self.move_straight(255)
        while not self.is_wall_left_b():
            self.move_straight(255)
        time.sleep(self.corner_step)

    def shut_down(self):
        self.sensors_controller.shut_down()
