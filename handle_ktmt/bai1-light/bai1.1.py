import RPi.GPIO as GPIO
import time
import os

def main():
    LED = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    while True:
        if GPIO.input(LED) == GPIO.LOW:
            GPIO.output(LED,GPIO.HIGH)
            time.sleep(1)
        if GPIO.input(LED) == GPIO.HIGH:
            GPIO.output(LED,GPIO.LOW)
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()