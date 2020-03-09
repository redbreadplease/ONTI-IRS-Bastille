from MainController import RobotController
from Mapping import MapBuilder

rc = RobotController()
rc.do_any_align()

mb = MapBuilder()

rd = 0


def choose_next_direction():
    global rd, rc, mb
    around_cells_discovering_state = mb.get_last_around_cells_states()
    if (not rc.is_wall_front() and around_cells_discovering_state[0]) and \
            (not rc.is_wall_left() and around_cells_discovering_state[1]) and \
            (not rc.is_wall_back() and around_cells_discovering_state[2]) and \
            (not rc.is_wall_right() and around_cells_discovering_state[3]):
        rd = mb.get_direction_of_inverse_wave_trace()
    elif not rc.is_wall_front() and around_cells_discovering_state[0]:
        rd = 0
    elif not rc.is_wall_left() and around_cells_discovering_state[1]:
        rd = 1
    elif not rc.is_wall_back() and around_cells_discovering_state[2]:
        rd = 2
    elif not rc.is_wall_right() and around_cells_discovering_state[3]:
        rd = 3
    else:
        print("WHAT THE FUCK???")
        exit()


def update_map_builder():
    global rd, mb, rc
    mb.update(rd, mb.get_cells_driven_since_last_time_amount(), rc.get_walls_availability_array())


while not mb.is_map_built():
    if rd == 0:
        rc.while_state_move_straight()
        update_map_builder()
        choose_next_direction()
    if rd == 1:
        rc.while_state_move_left()
        update_map_builder()
        choose_next_direction()
    if rd == 2:
        rc.while_state_move_back()
        update_map_builder()
        choose_next_direction()
    if rd == 3:
        rc.while_state_move_right()
        update_map_builder()
        choose_next_direction()

print("YEAH")
exit()
