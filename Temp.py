from MainController import RobotController

rc = RobotController()

rc.do_any_align()

while not rc.is_cliff_right_f_started():
    rc.move_straight(255)

rc.stop_move()
