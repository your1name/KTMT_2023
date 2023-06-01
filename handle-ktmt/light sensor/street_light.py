import RPi.GPIO as GPIO 
import time
sensor = 5
rl_1 = 16
rl_2 = 12

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(rl_1, GPIO.OUT)
    GPIO.setup(rl_2, GPIO.OUT)
    while True:
        if GPIO.input(sensor) == 1:
            GPIO.output(rl_1, 1)
            for i in range(10):
                if GPIO.input(sensor) == 0:
                    GPIO.output(rl_1, 0)
                    GPIO.output(rl_2, 0)
                    break
                if i == 9:
                    GPIO.output(rl_2, 1)
                time.sleep(0.2)

        if GPIO.input(sensor) == 0:
            GPIO.output(rl_1, 0)
            GPIO.output(rl_2, 0)
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()