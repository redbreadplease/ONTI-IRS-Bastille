import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(26, 50)
p.start(0)
try:

    print(GPIO.input(21))
    if (GPIO.input(21) == 1):
        while (GPIO.input(21) == GPIO.HIGH):
            p.ChangeDutyCycle(7.5)
    while (GPIO.input(21) == GPIO.LOW):
        p.ChangeDutyCycle(7.5)

    p.ChangeDutyCycle(0)

    p.stop()
    GPIO.cleanup()

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
