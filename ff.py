import time
import VL53L0X
import RPi.GPIO as GPIO
import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)

global n
n = 0
old_n = 0
err_al = 7
err_d = 7
err_l = 50
kp1 = 9
kp2 = 9
kp3 = 1
dist_to_wall = 110
dist_to_wall2 = 80
min_v = 210
max_v = 550
l = 7750
l2 = 8250

iz_map = [["x" for i in range(35)] for i in range(35)]

for i in range(35):
    s = ""
    for j in range(35):
        if (i % 2 == 0) and (j % 2 == 0):
            iz_map[i][j] = "."

x_s = 17
y_s = 17

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 11
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 5
sensor3_shutdown = 12
sensor4_shutdown = 13
sensor5_shutdown = 17
sensor6_shutdown = 18
sensor7_shutdown = 27
sensor8_shutdown = 9

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
GPIO.setup(sensor3_shutdown, GPIO.OUT)
GPIO.setup(sensor4_shutdown, GPIO.OUT)
GPIO.setup(sensor5_shutdown, GPIO.OUT)
GPIO.setup(sensor6_shutdown, GPIO.OUT)
GPIO.setup(sensor7_shutdown, GPIO.OUT)
GPIO.setup(sensor8_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
GPIO.output(sensor3_shutdown, GPIO.LOW)
GPIO.output(sensor4_shutdown, GPIO.LOW)
GPIO.output(sensor5_shutdown, GPIO.LOW)
GPIO.output(sensor6_shutdown, GPIO.LOW)
GPIO.output(sensor7_shutdown, GPIO.LOW)
GPIO.output(sensor8_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

tof1 = VL53L0X.VL53L0X(address=0x5A)
tof2 = VL53L0X.VL53L0X(address=0x5B)
tof3 = VL53L0X.VL53L0X(address=0x5C)
tof4 = VL53L0X.VL53L0X(address=0x5E)
tof5 = VL53L0X.VL53L0X(address=0x5F)
tof6 = VL53L0X.VL53L0X(address=0x7A)
tof7 = VL53L0X.VL53L0X(address=0x6B)
tof8 = VL53L0X.VL53L0X(address=0x6C)

GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(3)

GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof2.start_ranging(3)

GPIO.output(sensor3_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof3.start_ranging(3)

GPIO.output(sensor4_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof4.start_ranging(3)

GPIO.output(sensor5_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof5.start_ranging(3)

GPIO.output(sensor6_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof6.start_ranging(3)

GPIO.output(sensor7_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof7.start_ranging(3)

GPIO.output(sensor8_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof8.start_ranging(3)

timing = tof1.get_timing()
if (timing < 20000):
    timing = 20000
print("Timing %d ms" % (timing / 1000))


def dist1():
    distance = tof1.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def dist2():
    distance = tof2.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def dist3():
    distance = tof3.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance + 10
    else:
        return 0


def dist4():
    distance = tof4.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def dist5():
    distance = tof5.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance - 20
    else:
        return 0


def dist6():
    distance = tof6.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def dist7():
    distance = tof7.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def dist8():
    distance = tof8.get_distance()
    if (distance > 0):
        if (distance > 1000):
            return 1000
        return distance
    else:
        return 0


def up(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write("0q" + str(abs(v)) + "w0e" + str(abs(v)) + "r0t" + str(abs(v)) + "y0u" + str(abs(v)) + "i")


def down(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write(str(abs(v)) + "q0w" + str(abs(v)) + "e0r" + str(abs(v)) + "t0y" + str(abs(v)) + "u0i")


def rotation_left(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write(str(abs(v)) + "q" + str(abs(v)) + "w0e" + str(abs(v)) + "r0t0y" + str(abs(v)) + "u0i")


def rotation_right(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write("0q0w" + str(abs(v)) + "e0r" + str(abs(v)) + "t" + str(abs(v)) + "y0u" + str(abs(v)) + "i")


def left(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write("0q0w" + str(abs(v)) + "e" + str(abs(v)) + "r0t0y" + str(abs(v)) + "u" + str(abs(v)) + "i")


def right(v):
    if (abs(v) < min_v):
        v = min_v
    if (abs(v) > max_v):
        v = max_v
    ser.write(str(abs(v)) + "q" + str(abs(v)) + "w0e0r" + str(abs(v)) + "t" + str(abs(v)) + "y0u0i")


def stop():
    ser.write("0q0w0e0r0t0y0u0i")


def go_up():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
    )
    a = ""
    while (a != "y"):
        a = ser.read()

    old_x = ""
    a = ""
    while a != "x":
        a = ser.read()
        if (a != "x"):
            old_x = old_x + a
    old_y = ""
    a = ""
    while a != "y":
        a = ser.read()
        if (a != "y"):
            old_y = old_y + a
    time.sleep(0.5)
    err = l
    while err / kp3 > err_l:
        x = ""
        a = ""
        while a != "x":
            a = ser.read()
            if (a != "x"):
                x = x + a
        y = ""
        a = ""
        while a != "y":
            a = ser.read()
            if (a != "y"):
                y = y + a
        err = (l - int(x) + int(old_x)) * kp3
        up(err)
    stop()


def go_down():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
    )
    a = ""
    while (a != "y"):
        a = ser.read()

    old_x = ""
    a = ""
    while a != "x":
        a = ser.read()
        if (a != "x"):
            old_x = old_x + a
    old_y = ""
    a = ""
    while a != "y":
        a = ser.read()
        if (a != "y"):
            old_y = old_y + a
    time.sleep(0.5)
    err = -l
    while err / kp3 < -err_l:
        x = ""
        a = ""
        while a != "x":
            a = ser.read()
            if (a != "x"):
                x = x + a
        y = ""
        a = ""
        while a != "y":
            a = ser.read()
            if (a != "y"):
                y = y + a
        err = (-l - int(x) + int(old_x)) * kp3
        print(err)
        down(err)
    stop()


def go_left():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
    )
    a = ""
    while (a != "y"):
        a = ser.read()

    old_x = ""
    a = ""
    while a != "x":
        a = ser.read()
        if (a != "x"):
            old_x = old_x + a
    old_y = ""
    a = ""
    while a != "y":
        a = ser.read()
        if (a != "y"):
            old_y = old_y + a
    time.sleep(0.5)
    err = -l2
    while err / kp3 < -err_l:
        x = ""
        a = ""
        while a != "x":
            a = ser.read()
            if (a != "x"):
                x = x + a
        y = ""
        a = ""
        while a != "y":
            a = ser.read()
            if (a != "y"):
                y = y + a
        err = (-l2 - int(y) + int(old_y)) * kp3
        print(err)
        left(err)
    stop()


def go_right():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
    )
    a = ""
    while (a != "y"):
        a = ser.read()

    old_x = ""
    a = ""
    while a != "x":
        a = ser.read()
        if (a != "x"):
            old_x = old_x + a
    old_y = ""
    a = ""
    while a != "y":
        a = ser.read()
        if (a != "y"):
            old_y = old_y + a
    time.sleep(0.5)
    err = l2
    while err / kp3 > err_l:
        x = ""
        a = ""
        while a != "x":
            a = ser.read()
            if (a != "x"):
                x = x + a
        y = ""
        a = ""
        while a != "y":
            a = ser.read()
            if (a != "y"):
                y = y + a
        err = (l2 - int(y) + int(old_y)) * kp3
        print(err)
        right(err)
    stop()


def check():
    if (dist1() + dist4()) / 2 < 300:
        iz_map[y_s - 1][x_s] = "-"
    else:
        iz_map[y_s - 1][x_s] = " "

    if (dist5() + dist8()) / 2 < 300:
        iz_map[y_s + 1][x_s] = "-"
    else:
        iz_map[y_s + 1][x_s] = " "

    if (dist3() + dist6()) / 2 < 300:
        iz_map[y_s][x_s + 1] = "|"
    else:
        iz_map[y_s][x_s + 1] = " "

    if (dist2() + dist7()) / 2 < 300:
        print(dist2())
        print(dist7())
        print("---")
        iz_map[y_s][x_s - 1] = "|"
    else:
        iz_map[y_s][x_s - 1] = " "


def next_it():
    global n
    if (n == 0):
        if (dist3() + dist6()) / 2 > 300:
            n = 3
        elif (dist1() + dist4()) / 2 > 300:
            n = 0
        elif (dist2() + dist7()) / 2 > 300:
            n = 1
        else:
            n = 2
    elif (n == 1):
        if (dist1() + dist4()) / 2 > 300:
            n = 0
        elif (dist2() + dist7()) / 2 > 300:
            n = 1
        elif (dist5() + dist8()) / 2 > 300:
            n = 2
        else:
            n = 3
    elif (n == 2):
        if (dist2() + dist7()) / 2 > 300:
            n = 1
        elif (dist5() + dist8()) / 2 > 300:
            n = 2
        elif (dist3() + dist6()) / 2 > 300:
            n = 3
        else:
            n = 0
    elif (n == 3):
        if (dist5() + dist8()) / 2 > 300:
            n = 2
        elif (dist3() + dist6()) / 2 > 300:
            n = 3
        elif (dist1() + dist4()) / 2 > 300:
            n = 0
        else:
            n = 1


def align():
    if (n == 2):
        while (abs(dist2() - dist7()) > err_al):
            err = (dist2() - dist7()) * kp1
            if (err > 0):
                rotation_left(err)
            if (err < 0):
                rotation_right(err)
        for i in range(10):
            err = (dist2() - dist7()) * kp1
            if (err > 0):
                rotation_left(err)
            if (err < 0):
                rotation_right(err)
        print((dist2() + dist7()) / 2 - dist_to_wall)
        while (abs((dist2() + dist7()) / 2 - dist_to_wall) > err_d):
            err = ((dist2() + dist7()) / 2 - dist_to_wall) * kp2
            if (err > 0):
                left(err)
            if (err < 0):
                right(err)
        for i in range(10):
            err = ((dist2() + dist7()) / 2 - dist_to_wall) * kp2
            if (err > 0):
                left(err)
            if (err < 0):
                right(err)
        stop()
    if (n == 0):
        while (abs(dist3() - dist6()) > err_al):
            err = (dist3() - dist6()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        for i in range(10):
            err = (dist3() - dist6()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        while (abs((dist3() + dist6()) / 2 - dist_to_wall) > err_d):
            err = ((dist3() + dist6()) / 2 - dist_to_wall) * kp2
            if (err > 0):
                right(err)
            if (err < 0):
                left(err)
        for i in range(10):
            err = ((dist3() + dist6()) / 2 - dist_to_wall) * kp2
            if (err > 0):
                right(err)
            if (err < 0):
                left(err)
        stop()
    if (n == 1):
        while (abs(dist1() - dist4()) > err_al):
            err = (dist1() - dist4()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        for i in range(10):
            err = (dist1() - dist4()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        while (abs((dist1() + dist4()) / 2 - dist_to_wall2) > err_d):
            err = ((dist1() + dist4()) / 2 - dist_to_wall2) * kp2
            if (err > 0):
                up(err)
            if (err < 0):
                down(err)
        for i in range(10):
            err = ((dist1() + dist4()) / 2 - dist_to_wall2) * kp2
            if (err > 0):
                up(err)
            if (err < 0):
                down(err)
        stop()
    if (n == 3):
        while (abs(dist5() - dist8()) > err_al):
            err = (dist5() - dist8()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        for i in range(10):
            err = (dist5() - dist8()) * kp1
            if (err > 0):
                rotation_right(err)
            if (err < 0):
                rotation_left(err)
        while (abs((dist5() + dist8()) / 2 - dist_to_wall2) > err_d):
            err = ((dist5() + dist8()) / 2 - dist_to_wall2) * kp2
            if (err > 0):
                down(err)
            if (err < 0):
                up(err)
        for i in range(10):
            err = ((dist5() + dist8()) / 2 - dist_to_wall2) * kp2
            if (err > 0):
                down(err)
            if (err < 0):
                up(err)
        stop()


check()
for i in range(35):
    s = ""
    for j in range(35):
        s = s + iz_map[i][j]
    print(s)
o = 0

while o < 100:

    if (old_n == 0):
        old_n = 4

    print(old_n)
    print(n)
    print("=====")
    if (old_n - n != 1):
        align()
    if (n == 0):
        go_up()
        y_s = y_s - 2
    if (n == 1):
        go_left()
        x_s = x_s - 2
    if (n == 2):
        go_down()
        y_s = y_s + 2
    if (n == 3):
        go_right()
        x_s = x_s + 2
    # if (n==0)and ((dist3()+dist6())/2<400):
    #   align()
    # if (n==1)and ((dist1()+dist4())/2<400):
    #    align()
    # if (n==2)and ((dist2()+dist7())/2<400):
    #   align()
    # if (n==3)and ((dist5()+dist8())/2<400):
    #    align()
    check()
    old_n = n
    next_it()
    o = o + 1
    for i in range(35):
        s = ""
        for j in range(35):
            s = s + iz_map[i][j]
        print(s)

for i in range(35):
    s = ""
    for j in range(35):
        s = s + iz_map[i][j]
    print(s)
