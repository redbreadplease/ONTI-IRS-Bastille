from RobotController import RobotController

rb = RobotController()

while True:
    input_code = int(input())
    if input_code == 1:
        for i in range(100):
            rb.do_front_align()
    if input_code == 2:
        for i in range(100):
            rb.do_left_align()
    if input_code == 3:
        for i in range(100):
            rb.do_back_align()
    if input_code == 4:
        for i in range(100):
            rb.do_right_align()
    if input_code == 0:
        rb.stop_move()
