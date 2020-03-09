from MainController import RobotController

rc = RobotController()

rc.move_straight(255)
while True:
    print(rc.get_front_bias())
