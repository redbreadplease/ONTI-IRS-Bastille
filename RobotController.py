import serial
import time
import VL53L0X
import RPi.GPIO as GPIO


class RobotController:
    sensor_front_r_id, sensor_front_l_id = 22, 27
    sensor_left_f_id, sensor_left_b_id = 10, 20
    sensor_back_r_id, sensor_back_l_id = 12, 16
    sensor_right_f_id, sensor_right_b_id = 4, 8
    tof_front_r, tof_front_l = VL53L0X.VL53L0X(address=0x2A), VL53L0X.VL53L0X(address=0x2B)
    tof_left_f, tof_left_b = VL53L0X.VL53L0X(address=0x2C), VL53L0X.VL53L0X(address=0x2D)
    tof_back_r, tof_back_l = VL53L0X.VL53L0X(address=0x2E), VL53L0X.VL53L0X(address=0x2F)
    tof_right_f, tof_right_b = VL53L0X.VL53L0X(address=0x4A), VL53L0X.VL53L0X(address=0x4E)

    sensors_ids_and_tofs = [[sensor_right_f_id, tof_right_f], [sensor_right_b_id, tof_right_b],
                            [sensor_left_f_id, tof_left_f], [sensor_left_b_id, tof_left_b],
                            [sensor_front_r_id, tof_front_r], [sensor_front_l_id, tof_front_l],
                            [sensor_back_r_id, tof_back_r], [sensor_back_l_id, tof_back_l]]

    P_koef = 3.0
    right_distance = 150
    min_react_value = 30
    wall_dist_deviation = 30

    def __init__(self):
        self.is_align_finished = False
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for sensor_id, _ in self.sensors_ids_and_tofs:
            GPIO.setup(sensor_id, GPIO.OUT)
            GPIO.output(sensor_id, GPIO.LOW)
        time.sleep(0.50)
        for sensor_id, sensor_tof in self.sensors_ids_and_tofs:
            GPIO.output(sensor_id, GPIO.HIGH)
            time.sleep(0.50)
            sensor_tof.start_ranging(4)

        self.timing = self.tof_front_r.get_timing()
        if self.timing < 20000:
            self.timing = 20000
        print("Timing %d ms" % (self.timing / 1000))

    def do_front_align(self):
        d1, d2 = self.tof_front_l.get_distance(), self.tof_front_r.get_distance()
        err = round((max(min(abs(d1 - d2) * self.P_koef, 255), 0)), 1)
        if d1 - d2 > self.min_react_value:
            self.is_align_finished = False
            self.move_clockwise(err)
        elif d2 - d1 > self.min_react_value:
            self.is_align_finished = False
            self.move_counterclockwise(err)
        else:
            diff = (d1 + d2) / 2.
            if diff > self.right_distance + self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_straight(diff - self.right_distance)
            elif diff < self.right_distance - self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_back(diff - self.right_distance)
            else:
                self.is_align_finished = True

    def do_left_align(self):
        d1, d2 = self.tof_left_f.get_distance(), self.tof_left_b.get_distance()
        err = round((max(min(abs(d1 - d2) * self.P_koef, 255), 0)), 1)
        if d1 - d2 > self.min_react_value:
            self.is_align_finished = False
            self.move_counterclockwise(err)
        elif d2 - d1 > self.min_react_value:
            self.is_align_finished = False
            self.move_clockwise(err)
        else:
            diff = (d1 + d2) / 2.
            if diff > self.right_distance + self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_left(diff - self.right_distance)
            elif diff < self.right_distance - self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_right(diff - self.right_distance)
            else:
                self.is_align_finished = True

    def do_back_align(self):
        d1, d2 = self.tof_back_l.get_distance(), self.tof_back_r.get_distance()
        err = round((max(min(abs(d1 - d2) * self.P_koef, 255), 0)), 1)
        if d1 - d2 > self.min_react_value:
            self.is_align_finished = False
            self.move_counterclockwise(err)
        elif d2 - d1 > self.min_react_value:
            self.is_align_finished = False
            self.move_clockwise(err)
        else:
            diff = (d1 + d2) / 2.
            if diff > self.right_distance + self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_back(diff - self.right_distance)
            elif diff < self.right_distance - self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_straight(diff - self.right_distance)
            else:
                self.is_align_finished = True

    def do_right_align(self):
        d1, d2 = self.tof_right_b.get_distance(), self.tof_right_f.get_distance()
        err = round((max(min(abs(d1 - d2) * self.P_koef, 255), 0)), 1)
        print(str(d1) + " " + str(d2))
        if d1 - d2 > self.min_react_value:
            self.is_align_finished = False
            self.move_counterclockwise(err)
        elif d2 - d1 > self.min_react_value:
            self.is_align_finished = False
            self.move_clockwise(err)
        else:
            diff = (d1 + d2) / 2.
            print(str(diff) + " " + str(d1) + " " + str(d2))
            if diff > self.right_distance + self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_right(diff - self.right_distance)
            elif diff < self.right_distance - self.wall_dist_deviation:
                self.is_align_finished = False
                self.move_left(diff - self.right_distance)
            else:
                self.is_align_finished = True

    def move_clockwise(self, value):
        self.signal_to_move(value, value, 0, value, 0, value, 0, 0)

    def move_counterclockwise(self, value):
        self.signal_to_move(0, 0, value, 0, value, 0, value, value)

    def is_align_finished(self):
        return self.is_align_finished

    def move_back(self, val):
        self.signal_to_move(0, val, val, 0, val, val, 0, 0)

    def move_right(self, val):
        self.signal_to_move(val, val, 0, 0, val, 0, val, 0)

    def move_straight(self, val):
        self.signal_to_move(val, 0, 0, val, 0, 0, val, val)

    def move_left(self, val):
        self.signal_to_move(0, 0, val, val, 0, val, 0, val)

    def is_wall_front(self):
        return (self.tof_front_r.get_distance() + self.tof_front_l.get_distance()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_left(self):
        return (self.tof_left_b.get_distance() + self.tof_left_f.get_distance()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_back(self):
        return (self.tof_back_l.get_distance() + self.tof_back_r.get_distance()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def is_wall_right(self):
        return (self.tof_right_b.get_distance() + self.tof_right_f.get_distance()) / 2. < \
               self.right_distance + self.wall_dist_deviation

    def stop_move(self):
        self.signal_to_move(0, 0, 0, 0, 0, 0, 0, 0)

    def is_align_front_necessary(self):
        d1, d2 = self.tof_front_l.get_distance(), self.tof_front_r.get_distance()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_left_necessary(self):
        d1, d2 = self.tof_left_b.get_distance(), self.tof_left_f.get_distance()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_back_necessary(self):
        d1, d2 = self.tof_back_l.get_distance(), self.tof_back_r.get_distance()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def is_align_right_necessary(self):
        d1, d2 = self.tof_right_f.get_distance(), self.tof_right_b.get_distance()
        if abs(d1 - d2) > self.min_react_value or abs((d1 + d2) / 2. - self.right_distance) > self.wall_dist_deviation:
            return True
        else:
            return False

    def signal_to_move(self, a1, a2, b1, b2, c1, c2, d1, d2):
        self.ser.write(str(int(a1)) + "q" + str(int(a2)) + "w" + str(int(b1)) + "e" + str(int(b2)) + "r" + str(
            int(c1)) + "t" + str(int(c2)) + "y" + str(int(d1)) + "u" + str(int(d2)) + "i")

    def shut_down(self):
        self.tof_front_r.stop_ranging()
        GPIO.output(self.sensor_front_l_id, GPIO.LOW)
        self.tof_front_l.stop_ranging()
        GPIO.output(self.sensor_front_r_id, GPIO.LOW)


n = 0
r = RobotController()

while True:
    if n == 0:
        if r.is_align_right_necessary():
            r.do_right_align()
            print("r_al")
        if r.is_align_finished:
            r.move_straight(255)
            print("s_m")
        if r.is_wall_front():
            print("1")
            r.stop_move()
            n = 1

    elif n == 1:
        if r.is_align_front_necessary():
            r.do_front_align()
            print("f_al")
        if r.is_align_finished:
            r.move_left(255)
            print("l_m")
        if r.is_wall_left():
            print("2")
            r.stop_move()
            n = 2

    elif n == 2:
        if r.is_align_left_necessary():
            r.do_left_align()
            print("l_al")
        if r.is_align_finished:
            r.move_back(255)
            print("b_m")
        if r.is_wall_back():
            print("3")
            r.stop_move()
            n = 3

    elif n == 3:
        if r.is_align_back_necessary():
            r.do_back_align()
            print("b_al")
        if r.is_align_finished:
            r.move_right(255)
            print("r_m")
        if r.is_wall_right():
            print("4")
            r.stop_move()
            n = 0
