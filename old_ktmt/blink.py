# Viết chương trình nhấp nháy đèn xanh-đỏ theo chu kỳ 1s (xanh sáng-đỏ tắt...)
# bấm BT1 tất cả đèn đều tắt
import RPi.GPIO as GPIO
import time


def main():
    ispressBT1 = False
    BT1 = 14
    BLED = 1
    RLED = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BLED, GPIO.OUT)
    GPIO.setup(RLED, GPIO.OUT)
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            GPIO.output(BLED, GPIO.LOW)
            GPIO.output(RLED, GPIO.LOW)
            ispressBT1 = True
        if ispressBT1:
            continue
        if GPIO.input(BLED) == GPIO.LOW:
            GPIO.output(BLED, GPIO.HIGH)
            GPIO.output(RLED, GPIO.LOW)
            time.sleep(1)
        # elif GPIO.input(BLED) == GPIO.HIGH:
        else:
            GPIO.output(BLED, GPIO.LOW)
            GPIO.output(RLED, GPIO.HIGH)
            time.sleep(1)


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
