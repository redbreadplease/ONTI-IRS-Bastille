import time

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
        walls = self.get_walls_availability_array()
        aligns = [self.do_front_align, self.do_left_align, self.do_back_align, self.do_right_align]
        for i in range(4):
            if walls[i - 1] == walls[i]:
                for _ in range(2):
                    aligns[i - 1]()
                    aligns[i]()
                return
        '''
        for i in range(4):
            if walls[i]:
                aligns[i]()
                return
'''

    def handle_cliff(self, is_cliff_fading, is_wall_back_of_direction, move, leave_not_fading_cliff):
        if is_cliff_fading():
            print("cliff is fading")
            while is_wall_back_of_direction():
                move(self.just_move_value)
            print("ended moving following direction")
            time.sleep(0.2)
        else:
            print("cliff is not fading")
            leave_not_fading_cliff()
            time.sleep(0.2)
        self.stop_move()

    def while_state_move(self, clean_sensors_first, clean_sensors_second,
                         is_wall_following_direction, move_following_direction,
                         first_cliff_detected, leave_first_cliff,
                         second_cliff_detected, leave_second_cliff,
                         is_first_cliff_fading, is_second_cliff_fading,
                         is_wall_first_back_direction_sensor, is_wall_second_back_direction_sensor):
        clean_sensors_first()
        clean_sensors_second()
        while not is_wall_following_direction():
            self.update_sensors_queues()
            move_following_direction(self.just_move_value)
            if first_cliff_detected():
                self.handle_cliff(
                    is_first_cliff_fading, is_wall_first_back_direction_sensor, move_following_direction,
                    leave_first_cliff)
                return True
            elif second_cliff_detected():
                self.handle_cliff(
                    is_second_cliff_fading, is_wall_second_back_direction_sensor, move_following_direction,
                    leave_second_cliff)
                return True
        self.stop_move()
        return False

    def while_state_move_straight(self):
        return self.while_state_move(
            self.clean_back_sensors_queue, self.clean_front_sensors_queue,
            self.is_wall_front, self.move_straight,
            self.is_cliff_left_f_started, self.leave_front_l_around_corner,
            self.is_cliff_right_f_started, self.leave_front_r_around_corner,
            self.is_dist_left_f_bigger_then_b, self.is_idst_right_f_bigger_then_b,
            self.is_wall_left_b, self.is_wall_right_b
        )

    def while_state_move_right(self):
        return self.while_state_move(
            self.clean_left_sensors_queue, self.clean_right_sensors_queue,
            self.is_wall_right, self.move_right,
            self.is_cliff_front_r_started, self.leave_right_f_around_corner,
            self.is_cliff_back_r_started, self.leave_right_b_around_corner,
            self.is_dist_front_r_bigger_then_l, self.is_dist_back_r_bigger_then_l,
            self.is_wall_front_l, self.is_wall_back_l
        )

    def while_state_move_back(self):
        return self.while_state_move(
            self.clean_back_sensors_queue, self.clean_front_sensors_queue,
            self.is_wall_back, self.move_back,
            self.is_cliff_left_b_started, self.leave_back_l_around_corner,
            self.is_cliff_right_b_started, self.leave_back_r_around_corner,
            self.is_dist_left_b_bigger_then_f, self.is_dist_right_b_bigger_then_f,
            self.is_wall_left_f, self.is_wall_right_f
        )

    def while_state_move_left(self):
        return self.while_state_move(
            self.clean_left_sensors_queue, self.clean_right_sensors_queue,
            self.is_wall_left, self.move_left,
            self.is_cliff_front_l_started, self.leave_left_f_around_corner,
            self.is_cliff_back_l_started, self.leave_left_b_around_corner,
            self.is_dist_front_l_bigger_then_r, self.is_dist_back_l_bigger_then_r,
            self.is_wall_front_r, self.is_wall_back_r
        )
