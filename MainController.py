from Movement import MovementAlgorithms, AppliedMovement
from OpticalFlow import OpticalFlowController
from Sensors import SensorsController


class RobotController(MovementAlgorithms, AppliedMovement, SensorsController, OpticalFlowController):
    def __init__(self):
        super(MovementAlgorithms, self).__init__()
        super(AppliedMovement, self).__init__()
        super(SensorsController, self).__init__()
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
        self.clean_back_sensors_queue()
        self.clean_front_sensors_queue()
        while not self.is_wall_front():
            self.move_straight(self.just_move_value)
            if self.is_cliff_left_f_started():
                print("cliff_left_f started")
                self.leave_front_l_around_corner()
                return True
            elif self.is_cliff_right_f_started():
                print("cliff_right_f started")
                self.leave_front_r_around_corner()
                return True
        self.stop_move()
        return False

    def while_state_move_right(self):
        self.clean_left_sensors_queue()
        self.clean_right_sensors_queue()
        while not self.is_wall_right():
            self.move_right(self.just_move_value)
            if self.is_cliff_front_r_started():
                print("cliff_front_r started")
                self.leave_right_f_around_corner()
                return True
            elif self.is_cliff_back_r_started():
                print("cliff_back_r started")
                self.leave_right_b_around_corner()
                return True
        self.stop_move()
        return False

    def while_state_move_back(self):
        self.clean_back_sensors_queue()
        self.clean_front_sensors_queue()
        while not self.is_wall_back():
            self.move_back(self.just_move_value)
            if self.is_cliff_left_b_started():
                print("cliff_left_b started")
                self.leave_back_l_around_corner()
                return True
            elif self.is_cliff_right_b_started():
                print("cliff_right_b started")
                self.leave_back_r_around_corner()
                return True
        self.stop_move()
        return False

    def while_state_move_left(self):
        self.clean_left_sensors_queue()
        self.clean_right_sensors_queue()
        while not self.is_wall_left():
            self.move_left(self.just_move_value)
            if self.is_cliff_front_l_started():
                print("cliff_front_l started")
                self.leave_left_f_around_corner()
                return True
            elif self.is_cliff_back_l_started():
                print("cliff_back_l started")
                self.leave_left_b_around_corner()
                return True
        self.stop_move()
        return False
