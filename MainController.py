from Movement import MovementAlgorithms
from OpticalFlow import OpticalFlowController


class RobotController(MovementAlgorithms, OpticalFlowController):
    def __init__(self):
        super(MovementAlgorithms, self).__init__()
        super(OpticalFlowController, self).__init__()

    def do_any_align(self):
        if self.is_wall_front():
            self.do_front_align()
        elif self.is_wall_left():
            self.do_left_align()
        elif self.is_wall_back():
            self.do_back_align()
        elif self.is_wall_right():
            self.do_right_align()

    def while_state_move_straight(self):
        while not self.is_wall_front():
            self.move_straight(self.just_move_value)
            if self.is_cliff_left_started():
                self.leave_front_l_around_corner()
                return True
            elif self.is_cliff_right_started():
                self.leave_front_r_around_corner()
                return True
        return False

    def while_state_move_right(self):
        while not self.is_wall_right():
            self.move_right(self.just_move_value)
            if self.is_cliff_front_started():
                self.leave_right_f_around_corner()
                return True
            elif self.is_cliff_back_started():
                self.leave_right_b_around_corner()
                return True
        return False

    def while_state_move_back(self):
        while not self.is_wall_back():
            self.move_back(self.just_move_value)
            if self.is_cliff_left_started():
                self.leave_back_l_around_corner()
                return True
            elif self.is_cliff_right_started():
                self.leave_back_r_around_corner()
                return True
        return False

    def while_state_move_left(self):
        while not self.is_wall_left():
            self.move_left(self.just_move_value)
            if self.is_cliff_front_started():
                self.leave_left_f_around_corner()
                return True
            elif self.is_cliff_back_started():
                self.leave_left_b_around_corner()
                return True
        return False
