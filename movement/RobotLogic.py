class RobotLogic:
    def __init__(self):
        pass

    p_coefficient = 3.
    min_round_react_align_value = 10
    right_align_distance = 110
    align_dist_deviation = 20

    def get_align_err(self, d1, d2):
        return round((max(min(abs(d1 - d2) * self.p_coefficient, 255), 30)), 1)

    def does_side_sensors_difference_means_round_align(self, d1, d2):
        return d1 - d2 > self.min_round_react_align_value

    def does_side_sensors_difference_means_go_in_wall_direction(self, mid_value):
        return mid_value > self.right_align_distance + self.align_dist_deviation

    def does_side_sensors_difference_means_go_from_wall(self, mid_value):
        return mid_value > self.right_align_distance - self.align_dist_deviation

    @staticmethod
    def get_mid_value(a, b):
        return (a + b) / 2.

    def does_sensors_values(self, d1, d2):
        return self.get_mid_value(d1, d2) < self.right_align_distance + self.align_dist_deviation
