import RPi.GPIO as GPIO
import time
def main():
    BT4 = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    global s
    s = sg90() 
    #
    anglepulseBT4 =10
    print('all is ready')
    while True:
        if GPIO.input(BT4) == 0:
            print('quay 10 angle')
            controlservo(s, anglepulseBT4)
        time.sleep(0.2)

def controlservo(s, anglepulseBT):
    # sth cmt
    current = s.currentdirection()
    if current + anglepulseBT > 160:
        anglepulseBT = -current
    # if current + anglepulseBT > 160 or current + anglepulseBT < 0:
    #     anglepulseBT = -anglepulseBT
    
    current += anglepulseBT
    print(' goc hien tai:' + str(current) )
    s.setdirection(current, 10)
    time.sleep(0.5)
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
