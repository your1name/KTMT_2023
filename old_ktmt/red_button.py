# viết chương trình bấm BT1 lần 1 đèn đỏ sáng, bấm BT1 lần 2 đèn đỏ tắt, lặp đi lặp lại
import RPi.GPIO as GPIO
import time


def main():
    BT1 = 14
    LED = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED, GPIO.OUT)
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            if GPIO.input(LED) == GPIO.LOW:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(0.5)
            else:
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.5)


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
