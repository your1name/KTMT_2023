import RPi.GPIO as GPIO
import time

ispressBT1 = False
LED = 13



# Định nghĩa các callback
def bt1_callback(channel):
    global ispressBT1
    print("BT1 press")
    if not ispressBT1:
        ispressBT1 = True
        GPIO.output(LED, GPIO.HIGH)
    else:
        ispressBT1 = False
        GPIO.output(LED, GPIO.LOW)



def main():
    BT1 = 21
    GPIO.setmode(GPIO.BCM)  # setup mode

    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED, GPIO.OUT)

    GPIO.output(LED, GPIO.LOW)
    GPIO.add_event_detect(BT1, GPIO.FALLING, callback = bt1_callback, bouncetime=300)


if __name__ == '__main__':
    main()
