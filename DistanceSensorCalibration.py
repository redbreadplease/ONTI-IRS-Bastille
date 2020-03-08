# coding=utf-8

from Sensors import SensorsController

CALIBRATION_FILENAME = "distSensorsCalibration.txt"
valera_sensors = SensorsController()


def print_info():
    print
    "0 - калибровка по передней стороне Валеры"
    print
    "1 - калибровка по левой стороне Валеры"
    print
    "2 - калибровка по задней стороне Валеры"
    print
    "3 - калибровка по правой стороне Валеры"
    print
    "5 - показать содержимое"
    print
    "6 - завершить (нужно использовать, иначе Валере бывает плохо)"
    print
    ""


print_info()

dataFile = None

while True:
    try:
        fileRead = open(CALIBRATION_FILENAME, 'r')
        fileContent = fileRead.read().split("\n")
        fileRead.close()
        calibration_code = int(input())
        if calibration_code == 0:
            dataFile = open(CALIBRATION_FILENAME, 'w')
            val = str(valera_sensors.tof_front_l.get_distance() - valera_sensors.tof_front_r.get_distance())
            print
            "\ncalibration: " + val + "\n"
            dataFile.write("f_r " + val + "\n")
            for fileString in fileContent[1:]:
                dataFile.write(fileString + "\n")
            dataFile.close()
        elif calibration_code == 1:
            dataFile = open(CALIBRATION_FILENAME, 'w')
            for fileString in fileContent[:1]:
                dataFile.write(fileString + "\n")
            val = str(valera_sensors.tof_left_b.get_distance() - valera_sensors.tof_left_f.get_distance())
            print
            "\ncalibration: " + val + "\n"
            dataFile.write("l_f " + val + "\n")
            for fileString in fileContent[2:]:
                dataFile.write(fileString + "\n")
            dataFile.close()
        elif calibration_code == 2:
            dataFile = open(CALIBRATION_FILENAME, 'w')
            for fileString in fileContent[:2]:
                dataFile.write(fileString + "\n")
            val = str(valera_sensors.tof_back_r.get_distance() - valera_sensors.tof_back_l.get_distance())
            print
            "\ncalibration: " + val + "\n"
            dataFile.write("b_l " + val + "\n")
            for fileString in fileContent[3:]:
                dataFile.write(fileString + "\n")
            dataFile.close()
        elif calibration_code == 3:
            dataFile = open(CALIBRATION_FILENAME, 'w')
            for fileString in fileContent[:3]:
                dataFile.write(fileString + "\n")
            val = str(valera_sensors.tof_right_f.get_distance() - valera_sensors.tof_right_b.get_distance())
            print
            "\ncalibration: " + val + "\n"
            dataFile.write("r_b " + val + "\n")
            dataFile.close()
        elif calibration_code == 5:
            for fileString in fileContent:
                print
                fileString
        elif calibration_code == 6:
            print
            "Пока"
            valera_sensors.shut_down()
            exit()
        else:
            raise ValueError
    except SyntaxError:
        print
        "\n!!! Что-то не так с вводом. Попробуй ещё раз\n"
    except ValueError:
        print
        "\n!!! Что-то не так с вводом. Попробуй ещё раз\n"
    finally:
        print_info()
