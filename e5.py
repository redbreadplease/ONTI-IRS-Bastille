#!/usr/bin/env python
import time
import serial

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

# left front - to back  q
# right front - to front   w
# right front - to back   e
# left back - to front r
# left back - to back t
# right back - to front   y
# right back - to back u
# right back - to front i
