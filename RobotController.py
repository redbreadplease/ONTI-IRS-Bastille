from Movement import MovementAlgorithms
from Sensors import SensorsChecker
from Logic import LogicAlgorithms


class RobotController(SensorsChecker, MovementAlgorithms, LogicAlgorithms):
    def __init__(self):
        super().__init__()

    def is_wall_front(self):
        return self.is_wall(self.get_front_l_dist(), self.get_front_r_dist())

    def is_wall_left(self):
        return self.is_wall(self.get_left_f_dist(), self.get_left_b_dist())

    def is_wall_back(self):
        return self.is_wall(self.get_back_l_dist(), self.get_back_r_dist())

    def is_wall_right(self):
        return self.is_wall(self.get_right_f_dist(), self.get_right_b_dist())

    def do_any_align(self):
        if self.is_wall_front():
            self.do_front_align()
        elif self.is_wall_left():
            self.do_left_align()
        elif self.is_wall_back():
            self.do_back_align()
        elif self.is_wall_right():
            self.do_right_align()
