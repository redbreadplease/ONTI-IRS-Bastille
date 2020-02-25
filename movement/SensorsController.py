import VL53L0X
import RPi.GPIO as GPIO
import serial
import time


class SensorsController:
    CALIBRATION_FILENAME = "distSensorsCalibration.txt"

    sensor_front_r_id, sensor_front_l_id = 22, 27
    sensor_left_f_id, sensor_left_b_id = 10, 20
    sensor_back_r_id, sensor_back_l_id = 8, 16
    sensor_right_f_id, sensor_right_b_id = 4, 12
    tof_front_r, tof_front_l = VL53L0X.VL53L0X(address=0x2A), VL53L0X.VL53L0X(address=0x2B)
    tof_left_f, tof_left_b = VL53L0X.VL53L0X(address=0x2C), VL53L0X.VL53L0X(address=0x2D)
    tof_back_r, tof_back_l = VL53L0X.VL53L0X(address=0x2E), VL53L0X.VL53L0X(address=0x2F)
    tof_right_f, tof_right_b = VL53L0X.VL53L0X(address=0x4A), VL53L0X.VL53L0X(address=0x4F)

    sensors_ids_and_tofs = [[sensor_right_f_id, tof_right_f], [sensor_right_b_id, tof_right_b],
                            [sensor_left_f_id, tof_left_f], [sensor_left_b_id, tof_left_b],
                            [sensor_front_r_id, tof_front_r], [sensor_front_l_id, tof_front_l],
                            [sensor_back_r_id, tof_back_r], [sensor_back_l_id, tof_back_l]]

    def __init__(self):
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
        self.f_r_additive_dist, self.l_f_additive_dist, self.b_l_additive_dist, self.r_b_additive_dist = 0, 0, 0, 0
        calibration_file = open(self.CALIBRATION_FILENAME)
        calibration_file_context = calibration_file.read().split("\n")
        calibration_file.close()
        try:
            for calibrationFileString in calibration_file_context:
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
            print "No calibration sensors file found"
        self.prev_front_r_value, self.prev_front_l_value, self.prev_left_f_value, self.prev_left_b_value, \
        self.prev_back_l_value, self.prev_back_r_value, self.prev_right_b_value, self.prev_right_f_value \
            = self.tof_front_r.get_distance(), self.tof_front_l.get_distance(), \
              self.tof_left_f.get_distance(), self.tof_left_b.get_distance(), \
              self.tof_back_l.get_distance(), self.tof_back_r.get_distance(), \
              self.tof_right_b.get_distance(), self.tof_right_f.get_distance()

    def get_front_r_dist(self):
        self.prev_front_r_value = self.tof_front_r.get_distance()
        return self.prev_front_r_value + self.f_r_additive_dist

    def get_front_l_dist(self):
        self.prev_front_l_value = self.tof_front_l.get_distance()
        return self.prev_front_l_value

    def get_left_f_dist(self):
        self.prev_left_f_value = self.tof_left_f.get_distance()
        return self.prev_left_f_value + self.l_f_additive_dist

    def get_left_b_dist(self):
        self.prev_left_b_value = self.tof_left_b.get_distance()
        return self.prev_left_b_value

    def get_back_l_dist(self):
        self.prev_back_l_value = self.tof_back_l.get_distance()
        return self.prev_back_l_value + self.b_l_additive_dist

    def get_back_r_dist(self):
        self.prev_back_r_value = self.tof_back_r.get_distance()
        return self.prev_back_r_value

    def get_right_b_dist(self):
        self.prev_right_b_value = self.tof_right_b.get_distance()
        return self.prev_right_b_value + self.r_b_additive_dist

    def get_right_f_dist(self):
        self.prev_right_f_value = self.tof_right_f.get_distance()
        return self.prev_right_f_value

    def signal_to_move(self, a1, a2, b1, b2, c1, c2, d1, d2):
        self.ser.write(str(int(a1)) + "q" + str(int(a2)) + "w" + str(int(b1)) + "e" + str(int(b2)) + "r" + str(
            int(c1)) + "t" + str(int(c2)) + "y" + str(int(d1)) + "u" + str(int(d2)) + "i")

    def shut_down(self):
        self.tof_front_r.stop_ranging()
        GPIO.output(self.sensor_front_l_id, GPIO.LOW)
        self.tof_front_l.stop_ranging()
        GPIO.output(self.sensor_front_r_id, GPIO.LOW)
