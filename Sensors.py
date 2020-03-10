import VL53L0X
import RPi.GPIO as GPIO
import time
from Logic import LogicAlgorithms


class SensorsChecker(object):
    CALIBRATION_FILENAME = "distSensorsCalibration.txt"

    min_cliff_value = 50

    sensor_front_r_id, sensor_front_l_id = 12, 5
    sensor_left_f_id, sensor_left_b_id = 11, 9
    sensor_back_r_id, sensor_back_l_id = 18, 27
    sensor_right_f_id, sensor_right_b_id = 13, 17
    tof_front_r, tof_front_l = VL53L0X.VL53L0X(address=0x2A), VL53L0X.VL53L0X(address=0x2B)
    tof_left_f, tof_left_b = VL53L0X.VL53L0X(address=0x2C), VL53L0X.VL53L0X(address=0x2D)
    tof_back_r, tof_back_l = VL53L0X.VL53L0X(address=0x2E), VL53L0X.VL53L0X(address=0x2F)
    tof_right_f, tof_right_b = VL53L0X.VL53L0X(address=0x4A), VL53L0X.VL53L0X(address=0x4F)

    sensors_values_queue_size = 5

    sensors_ids_and_tofs = [[sensor_right_f_id, tof_right_f], [sensor_right_b_id, tof_right_b],
                            [sensor_left_f_id, tof_left_f], [sensor_left_b_id, tof_left_b],
                            [sensor_front_r_id, tof_front_r], [sensor_front_l_id, tof_front_l],
                            [sensor_back_r_id, tof_back_r], [sensor_back_l_id, tof_back_l]]

    def __init__(self):
        self.f_r_additive_dist, self.l_f_additive_dist, self.b_l_additive_dist, self.r_b_additive_dist = 0, 0, 0, 0
        calibration_file = open(self.CALIBRATION_FILENAME)
        calibration_file_context = calibration_file.read().split("\n")
        calibration_file.close()
        try:
            for calibrationFileString in calibration_file_context:
                if not calibrationFileString:
                    continue
                sensor_declaration, additive_value = calibrationFileString.split(" ")
                additive_value = int(additive_value)
                if sensor_declaration == 'f_r':
                    self.f_r_additive_dist = additive_value
                elif sensor_declaration == 'l_f':
                    self.l_f_additive_dist = additive_value
                elif sensor_declaration == 'b_l':
                    self.b_l_additive_dist = additive_value
                elif sensor_declaration == 'r_b':
                    self.r_b_additive_dist = additive_value
        except ValueError:
            print("No calibration sensors file found")
        self.prev_front_r_values, self.prev_front_l_values, self.prev_left_f_values, self.prev_left_b_values, \
        self.prev_back_l_values, self.prev_back_r_values, self.prev_right_b_values, self.prev_right_f_values \
            = list(), list(), list(), list(), list(), list(), list(), list()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for sensor_id, _ in self.sensors_ids_and_tofs:
            GPIO.setup(sensor_id, GPIO.OUT)
            GPIO.output(sensor_id, GPIO.LOW)
        time.sleep(0.3)
        for sensor_id, sensor_tof in self.sensors_ids_and_tofs:
            GPIO.output(sensor_id, GPIO.HIGH)
            time.sleep(0.3)
            sensor_tof.start_ranging(4)

        self.timing = self.tof_front_r.get_timing()
        if self.timing < 20000:
            self.timing = 20000
        print("Timing %d ms" % (self.timing / 1000))

    def get_dist(self, queue, tof, additive):
        queue.append(tof.get_distance())
        if len(queue) > self.sensors_values_queue_size:
            queue.remove(queue[0])
        return queue[-1] + additive

    def get_front_r_dist(self):
        return self.get_dist(self.prev_front_r_values, self.tof_front_r, self.f_r_additive_dist)

    def get_front_l_dist(self):
        return self.get_dist(self.prev_front_l_values, self.tof_front_l, 0)

    def get_left_f_dist(self):
        return self.get_dist(self.prev_left_f_values, self.tof_left_f, self.l_f_additive_dist)

    def get_left_b_dist(self):
        return self.get_dist(self.prev_left_b_values, self.tof_left_b, 0)

    def get_back_l_dist(self):
        return self.get_dist(self.prev_back_l_values, self.tof_back_l, self.b_l_additive_dist)

    def get_back_r_dist(self):
        return self.get_dist(self.prev_back_r_values, self.tof_back_r, 0)

    def get_right_b_dist(self):
        return self.get_dist(self.prev_right_b_values, self.tof_right_b, self.r_b_additive_dist)

    def get_right_f_dist(self):
        return self.get_dist(self.prev_right_f_values, self.tof_right_f, 0)

    def shut_down(self):
        for sensor_id, sensor_tof in self.sensors_ids_and_tofs:
            sensor_tof.stop_ranging()
            time.sleep(0.5)
            GPIO.output(sensor_id, GPIO.HIGH)


class SensorsController(SensorsChecker, LogicAlgorithms):
    def __init__(self):
        super(SensorsChecker, self).__init__()
        super(LogicAlgorithms, self).__init__()

    def is_wall_front(self):
        return self.is_wall(self.get_front_l_dist(), self.get_front_r_dist())

    def is_wall_left(self):
        return self.is_wall(self.get_left_f_dist(), self.get_left_b_dist())

    def is_wall_back(self):
        return self.is_wall(self.get_back_l_dist(), self.get_back_r_dist())

    def is_wall_right(self):
        return self.is_wall(self.get_right_f_dist(), self.get_right_b_dist())

    def is_wall_front_l(self):
        return self.is_wall_by_dist(self.get_front_l_dist())

    def is_wall_front_r(self):
        return self.is_wall_by_dist(self.get_front_r_dist())

    def is_wall_left_f(self):
        return self.is_wall_by_dist(self.get_left_f_dist())

    def is_wall_left_b(self):
        return self.is_wall_by_dist(self.get_left_b_dist())

    def is_wall_back_r(self):
        return self.is_wall_by_dist(self.get_back_r_dist())

    def is_wall_back_l(self):
        return self.is_wall_by_dist(self.get_back_l_dist())

    def is_wall_right_b(self):
        return self.is_wall_by_dist(self.get_right_b_dist())

    def is_wall_right_f(self):
        return self.is_wall_by_dist(self.get_right_f_dist())

    def is_cliff_started(self, first_tof, first_queue, second_tof):
        if first_tof.get_distance() - first_queue[0] > self.min_cliff_value:
            return first_tof.get_distance() - first_queue[0] > self.min_cliff_value
        return self.does_diff_mean_cliff(first_tof.get_distance(), second_tof.get_distance())

    def is_cliff_front_l_started(self):
        return self.is_cliff_started(self.tof_front_l, self.prev_front_l_values, self.tof_front_r)

    def is_cliff_front_r_started(self):
        return self.is_cliff_started(self.tof_front_r, self.prev_front_r_values, self.tof_front_l)

    def is_cliff_left_b_started(self):
        return self.is_cliff_started(self.tof_left_b, self.prev_left_b_values, self.tof_left_f)

    def is_cliff_left_f_started(self):
        return self.is_cliff_started(self.tof_left_f, self.prev_left_f_values, self.tof_left_b)

    def is_cliff_back_l_started(self):
        return self.is_cliff_started(self.tof_back_l, self.prev_back_l_values, self.tof_back_r)

    def is_cliff_back_r_started(self):
        return self.is_cliff_started(self.tof_back_r, self.prev_back_r_values, self.tof_back_l)

    def is_cliff_right_f_started(self):
        return self.is_cliff_started(self.tof_right_f, self.prev_right_f_values, self.tof_right_b)

    def is_cliff_right_b_started(self):
        return self.is_cliff_started(self.tof_right_b, self.prev_right_b_values, self.tof_right_f)

    def get_walls_availability_array(self):
        return [self.is_wall_front(), self.is_wall_left(), self.is_wall_back(), self.is_wall_right()]

    def clean_front_sensors_queue(self):
        self.prev_front_r_values, self.prev_front_l_values = list(), list()

    def clean_left_sensors_queue(self):
        self.prev_left_b_values, self.prev_left_f_values = list(), list()

    def clean_back_sensors_queue(self):
        self.prev_back_l_values, self.prev_back_r_values = list(), list()

    def clean_right_sensors_queue(self):
        self.prev_right_b_values, self.prev_right_f_values = list(), list()

    def clean_sensors_values_queues(self):
        self.clean_front_sensors_queue()
        self.clean_left_sensors_queue()
        self.clean_back_sensors_queue()
        self.clean_right_sensors_queue()
