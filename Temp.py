import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)
while True:
    x_now, y_now = "", ""
    while True:
        symbol = ser.read()

        if symbol != "x":
            x_now += symbol
        else:
            x_now = int(x_now)
            break
    while True:
        symbol = ser.read()

        if symbol != "y":
            y_now += symbol
        else:
            y_now = int(y_now)
            break
        print("x: " + str(x_now) + "  y: " + str(y_now))
