import RPi.GPIO as GPIO
import time
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    global s
    s = sg90() 
    #
    anglepulseBT1 =10
    anglepulseBT2 =50
    anglepulseBT3 =120
    print('all is ready')
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print('quay 10 angle')
            controlservo(s, anglepulseBT1)

        if GPIO.input(BT2) == GPIO.LOW:
            print('quay 50 angle')
            controlservo(s, anglepulseBT2)

        if GPIO.input(BT3) == GPIO.LOW:
            print('quay 120 angle')
            controlservo(s, anglepulseBT3)
        time.sleep(0.2)

def controlservo(s, anglepulseBT):
    # sth cmt
    current = s.currentdirection()
    if current + anglepulseBT > 160:
        current -= anglepulseBT
    else:
        current += anglepulseBT
    if current < 0:
        print('Illegal rotation')
        return anglepulseBT
    s.setdirection(current, 10)
    time.sleep(0.5)
    print(' goc hien tai:' + str(current) )
    return anglepulseBT

class sg90:
    def __init__(self):
        self.bin = 6 # define pin SERVO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bin, GPIO.OUT) # setup to  output
        self.servo = GPIO.PWM(self.bin, 50) # z is 50Hz
        self.servo.start(0.0) # start
        self.direction = 90
    def cleanup(self):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()
    def currentdirection(self):
        # display
        return self.direction
    def _henkan(self, value):
        # change value 0 - 180 to 2 - 12
        return round(0.056*value + 2.0)
    def setdirection(self, direction, speed):
        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction
try:
    main()
except KeyboardInterrupt:
    s.cleanup()
