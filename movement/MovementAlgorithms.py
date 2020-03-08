from movement.AppliedMovement import AppliedMovement
from sensors.SensorsChecker import SensorsChecker
from logic.LogicAlgorithms import LogicAlgorithms
import sys
import os

sys.path.insert(0, os.pardir)


class MovementAlgorithms(AppliedMovement):
    def __init__(self):
        self.sensors_checker = SensorsChecker()
        self.robot_logic = LogicAlgorithms()

    def do_front_align(self):
        while True:
            d1, d2 = self.sensors_checker.get_front_l_dist(), self.sensors_checker.get_front_r_dist()
            err = self.robot_logic.get_align_err(d1=d1, d2=d2)
            if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_clockwise(err)
            elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_counterclockwise(err)
            else:
                mid = self.robot_logic.get_mid_value(d1, d2)
                if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_straight(mid - self.robot_logic.right_align_distance)
                elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_back(mid - self.robot_logic.right_align_distance)
                else:
                    return

    def do_left_align(self):
        while True:
            d1, d2 = self.sensors_checker.get_left_f_dist(), self.sensors_checker.get_left_b_dist()
            err = self.robot_logic.get_align_err(d1=d1, d2=d2)
            if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.robot_logic.get_mid_value(d1, d2)
                if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_left(mid - self.robot_logic.right_align_distance)
                elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_right(mid - self.robot_logic.right_align_distance)
                else:
                    return

    def do_back_align(self):
        while True:
            d1, d2 = self.sensors_checker.get_back_l_dist(), self.sensors_checker.get_back_r_dist()
            err = self.robot_logic.get_align_err(d1=d1, d2=d2)
            if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.robot_logic.get_mid_value(d1, d2)
                if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_back(mid - self.robot_logic.right_align_distance)
                elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_straight(mid - self.robot_logic.right_align_distance)
                else:
                    return

    def do_right_align(self):
        while True:
            d1, d2 = self.sensors_checker.get_right_b_dist(), self.sensors_checker.get_right_f_dist()
            err = self.robot_logic.get_align_err(d1=d1, d2=d2)
            if self.robot_logic.does_side_sensors_difference_means_round_align(d1, d2):
                self.move_counterclockwise(err)
            elif self.robot_logic.does_side_sensors_difference_means_round_align(d2, d1):
                self.move_clockwise(err)
            else:
                mid = self.robot_logic.get_mid_value(d1, d2)
                if self.robot_logic.does_side_sensors_difference_means_go_in_wall_direction(mid):
                    self.move_right(mid - self.robot_logic.right_align_distance)
                elif self.robot_logic.does_side_sensors_difference_means_go_from_wall(mid):
                    self.move_left(mid - self.robot_logic.right_align_distance)
                else:
                    return
