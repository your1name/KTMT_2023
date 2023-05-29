# Viết chương trình đọc khoảng cách từ cảm biến siêu âm
# nếu khoảng cách < 10 cm thì bật đèn đỏ, > 10cm thì bật đèn xanh
import time
import RPi.GPIO as GPIO
import Adafruit_Nokia_LCD as LCD


def main():
    BT1 = 14
    TRIG = 16
    ECHO = 26

    RED = 22
    BLUE = 5

    global pulse_end

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(BLUE, GPIO.OUT)
    GPIO.output(TRIG, False)

    while True:

        print("Waiting For Sensor To Settle")

        time.sleep(2)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration*17150
        distance = round(distance, 2)

        if distance > 100:
            print("ERROR, try again")
        else:
            print("Distance: %scm" % distance)

            if distance < 10:
                GPIO.output(RED, GPIO.HIGH)
                GPIO.output(BLUE, GPIO.LOW)
            if distance > 10:
                GPIO.output(BLUE, GPIO.HIGH)
                GPIO.output(RED, GPIO.LOW)
        time.sleep(1)


try:
    main()

except KeyboardInterrupt:
    GPIO.cleanup()
