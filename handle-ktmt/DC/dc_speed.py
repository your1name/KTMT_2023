import RPi.GPIO as GPIO 
import time

def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20 
    BT4 = 19 
    DIR = 25
    PWD = 24
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2
    PWD1 = GPIO.PWM(DIR,100)
    PWD2 = GPIO.PWM(PWD,100)
    PWD1.start(0)
    PWD2.start(0)
    currentPWD1 = 20
    currentPWD2 = 20
    print("Chuan bi hoan tat ok")

    while True:
        if GPIO.input(BT1) == 0:
            print("Press BT1") 
            if currentPWD2 != 0:
                PWD2.ChangeDutyCycle(0)
                time.sleep(1)
            upPWD = int(0.2 * currentPWD1)
            currentPWD1 = (currentPWD1 + upPWD) if currentPWD1 + upPWD < 100 else 100
            if currentPWD1 == 0:
                currentPWD1 = 20
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Toc do hien tai: " + str(currentPWD1) + " theo chieu thuan")
            currentPWD2 = 0
            time.sleep(0.5)
        
        if GPIO.input(BT2) == 0:
            print("Press BT2") 
            PWD2.ChangeDutyCycle(0)
            downPWD = int(0.2 * currentPWD1)
            currentPWD1 = (currentPWD1 - downPWD) if currentPWD1 - downPWD > 0 else 0
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Toc do hien tai: " + str(currentPWD1) + " theo chieu thuan")
            currentPWD2 = 0
            time.sleep(0.5)

        if GPIO.input(BT3) == 0:
            print("Press BT3") 
            if currentPWD1 != 0:
                PWD1.ChangeDutyCycle(0)
                time.sleep(1)
            upPWD = int(20 / 100 * currentPWD2)
            currentPWD2 = (currentPWD2 + upPWD) if currentPWD2 + upPWD < 100 else 100
            if currentPWD2 == 0:
                currentPWD2 = 20
            PWD2.ChangeDutyCycle(currentPWD2)
            print("Toc do hien tai: -" + str(currentPWD2))
            currentPWD1 = 0
            time.sleep(0.5)
            
        if GPIO.input(BT4) == 0:
            print("Press BT4") 
            PWD1.ChangeDutyCycle(0)
            downPWD = int(20 / 100 * currentPWD2)
            currentPWD2 = (currentPWD2 - downPWD) if currentPWD2 - downPWD > 0 else 0
            print("Toc do hien tai: -" + str(currentPWD2))
            PWD2.ChangeDutyCycle(currentPWD2)
            currentPWD1 = 0
            time.sleep(0.5)


try:
    main()
except KeyboardInterrupt:
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()     
