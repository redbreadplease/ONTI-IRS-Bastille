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
        walls = [self.is_wall_front(), self.is_wall_left(), self.is_wall_back(), self.is_wall_right()]
        aligns = [self.do_front_align, self.do_left_align, self.do_back_align, self.do_right_align]
        for i in range(4):
            if walls[i - 1] == walls[i]:
                for _ in range(2):
                    aligns[i - 1]()
                    aligns[i]()

    def while_state_move(self, clean_sensors_first, clean_sensors_second, is_wall_following_direction,
                         move_following_direction, first_cliff_detected, leave_first_cliff, second_cliff_detected,
                         leave_second_cliff):
        clean_sensors_first()
        clean_sensors_second()
        while not is_wall_following_direction():
            move_following_direction(self.just_move_value)
            if first_cliff_detected():
                leave_first_cliff()
                return True
            elif second_cliff_detected():
                leave_second_cliff()
                return True
        self.stop_move()
        return False

    def while_state_move_straight(self):
        return self.while_state_move(
            self.clean_back_sensors_queue, self.clean_front_sensors_queue, self.is_wall_front, self.move_straight,
            self.is_cliff_left_f_started, self.leave_front_l_around_corner, self.is_cliff_right_f_started,
            self.leave_front_r_around_corner
        )

    def while_state_move_right(self):
        return self.while_state_move(
            self.clean_left_sensors_queue, self.clean_right_sensors_queue, self.is_wall_right, self.move_right,
            self.is_cliff_front_r_started, self.leave_right_f_around_corner, self.is_cliff_back_r_started,
            self.leave_right_b_around_corner
        )

    def while_state_move_back(self):
        return self.while_state_move(
            self.clean_back_sensors_queue, self.clean_front_sensors_queue, self.is_wall_back, self.move_back,
            self.is_cliff_left_b_started, self.leave_back_l_around_corner, self.is_cliff_right_b_started,
            self.leave_back_r_around_corner
        )

    def while_state_move_left(self):
        return self.while_state_move(
            self.clean_left_sensors_queue, self.clean_right_sensors_queue, self.is_wall_left, self.move_left,
            self.is_cliff_front_l_started, self.leave_left_f_around_corner, self.is_cliff_back_l_started,
            self.leave_left_b_around_corner
        )
