from RobotController import RobotController

opposite = {0: 2, 1: 3, 2: 0, 3: 1}

rc = RobotController()

turns = {}

rc.do_any_align()


def add_empty_dictionaries(prev_index):
    global rc, turns
    if prev_index != 2 and rc.is_wall_front():
        turns[0] = {}
    if prev_index != 3 and rc.is_wall_left():
        turns[1] = {}
    if prev_index != 0 and rc.is_wall_back():
        turns[2] = {}
    if prev_index != 1 and rc.is_wall_right():
        turns[3] = {}


def make_wave_trace(path):
    res_dict_value = turns[:]
    for index in path:
        res_dict_value = res_dict_value[index]
    if not res_dict_value:
        add_empty_dictionaries(path[-1])
    else:
        for key in res_dict_value.keys():
            if not res_dict_value[key]:
                copy = path[:]
                copy.append(key)
                make_wave_trace(copy)


add_empty_dictionaries(-1)
