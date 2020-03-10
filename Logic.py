class LogicAlgorithms(object):
    p_coefficient = 3.
    min_round_react_align_value = 10
    right_align_distance = 110
    align_dist_deviation = 20
    min_cliff_difference = 150
    wall_detection_distance = 200

    min_react_wheels_value = 255
    max_react_wheels_value = 511

    def get_align_progressive_err(self, d):
        return round((max(min(abs(d) * self.p_coefficient, self.max_react_wheels_value), self.min_react_wheels_value)),
                     1)

    def get_align_circle_err(self, d1, d2):
        return self.get_align_progressive_err(d1 - d2)

    def does_side_sensors_difference_means_round_align(self, d1, d2):
        return d1 - d2 > self.min_round_react_align_value

    def does_side_sensors_difference_means_go_in_wall_direction(self, mid_value):
        return mid_value > self.right_align_distance + self.align_dist_deviation

    def does_side_sensors_difference_means_go_from_wall(self, mid_value):
        return mid_value < self.right_align_distance - self.align_dist_deviation

    def is_wall(self, d1, d2):
        return self.get_mid_value(d1, d2) < self.wall_detection_distance

    def is_wall_by_dist(self, d):
        return d < self.wall_detection_distance

    @staticmethod
    def get_mid_value(a, b):
        return (a + b) / 2.

    def does_sensors_values(self, d1, d2):
        return self.get_mid_value(d1, d2) < self.right_align_distance + self.align_dist_deviation

    def does_mean_cliff_started(self, first_prev_dist, first_act_dist, second_prev_dist, second_act_dist):
        return (self.is_wall_by_dist(first_act_dist) or self.is_wall_by_dist(second_act_dist)) and abs(
            (first_prev_dist - first_act_dist) - (second_prev_dist - second_act_dist)) > self.min_cliff_difference

    def does_diff_mean_cliff(self, d1, d2):
        return abs(d1 - d2) > 150
