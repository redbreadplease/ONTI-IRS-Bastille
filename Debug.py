import time

from MainController import RobotController
import serial

from Sensors import SensorsController


def main():
    try:
        while True:
            print('########')
            print('\nDebug scripts:\n')
            print('\n0 - Temp\n')
            print('\n1 - e5\n')
            print('\n2 - волновая трассировка\n')
            print('\n3 - выравнивание\n')
            print('\n4 - калибровка optical flow\n')
            print('\n5 - калибровка датчиков')
            print('########')
            try:
                code = int(input())
                if code == 0:
                    test_temp()
                elif code == 1:
                    test_e5()
                elif code == 2:
                    test_wave_trace()
                elif code == 3:
                    test_align()
                else:
                    raise ValueError
            except ValueError:
                print('\nЧто-то не так с вводом. попробуйте ещё\n')
                continue
    except KeyboardInterrupt:
        print('\nПока\n')


def test_e5():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    counter = 0

    while 1:
        mode = input()
        if mode == 1:
            ser.write("0q511w0e511r0t511y0u511i")
        if mode == 2:
            ser.write("511q0w511e0r511t0y511u0i")
        if mode == 3:
            ser.write("511q511w0e511r0t0y511u0i")
        if mode == 4:
            ser.write("0q0w511e0r511t511y0u511i")
        if mode == 5:
            ser.write("511q511w0e0r511t511y0u0i")
        if mode == 6:
            ser.write("0q0w511e511r0t0y511u511i")
        if mode == 0:
            ser.write("0q0w0e0r0t0y0u0i")


def test_temp():
    rc = RobotController()

    rc.do_any_align()

    print("done")


def test_align():
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


def test_wave_trace():
    print('\nRun TWaveTrace.py - file\n')


def calibration_optical_flow():
    right_dist_drive, dist_now = 1300, 0
    inverse_moving = False

    robot_controller = RobotController()

    robot_controller.move_straight(255)
    time.sleep(0.1)

    if robot_controller.get_bias_x_y()[0] < 0:
        inverse_moving = True

    print("inverse: " + str(inverse_moving))

    while True:
        try:
            try:
                dist_now += robot_controller.get_bias_x_y()[1]
            except Exception:
                dist_now += robot_controller.get_bias_x_y()[1]
            print("                                                               dist: " + str(dist_now))
            print("Row optical flow values: " + str(robot_controller.get_optical_flow_row_values()))

            if dist_now > right_dist_drive:
                if not inverse_moving:
                    robot_controller.move_straight(255)
                else:
                    robot_controller.move_back(255)
                print("Moving minus")
            elif dist_now < -right_dist_drive:
                if not inverse_moving:
                    robot_controller.move_back(255)
                else:
                    robot_controller.move_straight(255)
                print("Moving plus")
        except ValueError:
            continue


def calibration_sensors():
    calibration_filename = "distSensorsCalibration.txt"
    valera_sensors = SensorsController()

    print("0 - калибровка по передней стороне Валеры")
    print("1 - калибровка по левой стороне Валеры")
    print("2 - калибровка по задней стороне Валеры")
    print("3 - калибровка по правой стороне Валеры")
    print("5 - показать содержимое")
    print("6 - завершить (нужно использовать, иначе Валере бывает плохо)")
    print()

    data_file = None

    while True:
        try:
            file_read = open(calibration_filename, 'r')
            file_content = file_read.read().split("\n")
            file_read.close()
            calibration_code = int(input())
            if calibration_code == 0:
                data_file = open(calibration_filename, 'w')
                val = str(valera_sensors.tof_front_l.get_distance() - valera_sensors.tof_front_r.get_distance())
                print("\ncalibration: " + val + "\n")
                data_file.write("f_r " + val + "\n")
                for fileString in file_content[1:]:
                    data_file.write(fileString + "\n")
                data_file.close()
            elif calibration_code == 1:
                data_file = open(calibration_filename, 'w')
                for fileString in file_content[:1]:
                    data_file.write(fileString + "\n")
                val = str(valera_sensors.tof_left_b.get_distance() - valera_sensors.tof_left_f.get_distance())
                print("\ncalibration: " + val + "\n")
                data_file.write("l_f " + val + "\n")
                for fileString in file_content[2:]:
                    data_file.write(fileString + "\n")
                data_file.close()
            elif calibration_code == 2:
                data_file = open(calibration_filename, 'w')
                for fileString in file_content[:2]:
                    data_file.write(fileString + "\n")
                val = str(valera_sensors.tof_back_r.get_distance() - valera_sensors.tof_back_l.get_distance())
                print("\ncalibration: " + val + "\n")
                data_file.write("b_l " + val + "\n")
                for fileString in file_content[3:]:
                    data_file.write(fileString + "\n")
                data_file.close()
            elif calibration_code == 3:
                data_file = open(calibration_filename, 'w')
                for fileString in file_content[:3]:
                    data_file.write(fileString + "\n")
                val = str(valera_sensors.tof_right_f.get_distance() - valera_sensors.tof_right_b.get_distance())
                print("\ncalibration: " + val + "\n")
                data_file.write("r_b " + val + "\n")
                data_file.close()
            elif calibration_code == 5:
                for fileString in file_content:
                    print(fileString)
            elif calibration_code == 6:
                print("Пока")
                valera_sensors.shut_down()
                exit()
            else:
                raise ValueError
        except SyntaxError:
            print("\n!!! Что-то не так с вводом. Попробуй ещё раз\n")
        except ValueError:
            print("\n!!! Что-то не так с вводом. Попробуй ещё раз\n")
        finally:
            print("0 - калибровка по передней стороне Валеры")
            print("1 - калибровка по левой стороне Валеры")
            print("2 - калибровка по задней стороне Валеры")
            print("3 - калибровка по правой стороне Валеры")
            print("5 - показать содержимое")
            print("6 - завершить (нужно использовать, иначе Валере бывает плохо)")
            print()


main()
