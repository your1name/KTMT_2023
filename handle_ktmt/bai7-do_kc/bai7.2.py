import RPi.GPIO as GPIO
import time
def main():
    BT1 = 21
    TRIG = 15
    ECHO = 4
    rl_1 = 16
    global pulse_end
    GPIO.setmode(GPIO.BCM)
    # khởi tạo và pull các bút bấm
    GPIO.setup(BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(rl_1, GPIO.OUT)
    GPIO.setup(TRIG, False)
    while GPIO.input(BT1) != 0:
        time.sleep(0.2)
    print('Bắt đâif mô phỏng cảm biến lùi ô tô')
    while True:
        # waiting for sensor to settle
        time.sleep(1)
        # bat, tat song am
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        # tinh thoi gian
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
            # tich khoang cach
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        print("Distance: %scm" % distance)
        if distance <= 4:
            GPIO.output(rl_1, 1)
            print("Distance: %scm" % distance)

        else:
            GPIO.output(rl_1, False)
        time.sleep(1)
        
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()