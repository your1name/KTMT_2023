import RPi.GPIO as GPIO
import time

def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global s
    s = sg90()
    anglepulseBT1 = 10
    anglepulseBT2 = 50
    anglepulseBT3 = 120
    print("Tat ca da san sang")
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("Quay 10 angle")
            controlservo(s, anglepulseBT1)
        if GPIO.input(BT2) == GPIO.LOW:
            print("Quay 50 angle")
            controlservo(s, anglepulseBT2)
        if GPIO.input(BT3) == GPIO.LOW:
            print("Quay 120 angle")
            controlservo(s, anglepulseBT3)
        time.sleep(0.2)

def controlservo(s, anglepulseBT):
    current = s.currentdirection()
    if current + anglepulseBT > 160:
        current -= anglepulseBT
    else:
        current += anglepulseBT
    if current < 0:
        print("Illegal rotation")
        return anglepulseBT
    s.setdirection(current, 10)
    time.sleep(0.5)
    return anglepulseBT

class sg90:
    def __init__(self):
        self.pin = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)
        self.direction = 90

    def cleanup(self):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection(self):
        return self.direction
    
    def _henkan(self, value):
        return round(0.056 * value + 2.0)
    
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