from MainController import RobotController

rc = RobotController()

while True:
    rc.do_right_align()

rc.move_right(255)
while True:
    print(rc.get_right_bias())
