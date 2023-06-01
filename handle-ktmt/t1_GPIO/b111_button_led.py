import RPi.GPIO as GPIO
import time 
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20 
    BT4 = 19 
    LED = 13
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.HIGH)
    ispressedBT4 = False
    ispressedBT3 = False
    countBT4 = 0
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("BT1 press")
            ispressedBT3 = False
            GPIO.output(LED, GPIO.LOW)
            time.sleep(0.5)
        if GPIO.input(BT2) == GPIO.LOW:
            print("BT2 press")
            ispressedBT3 = False
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(0.5)
        if GPIO.input(BT3) == GPIO.LOW:
            print("BT3 press")
            ispressedBT3 = True
        if GPIO.input(BT4) == GPIO.LOW:
            print("BT4 press")
            ispressedBT3 = False
            ispressedBT4 = True
            countBT4+=1
            if ispressedBT4: 
                if countBT4 % 2 == 1:  
                    GPIO.output(LED, GPIO.HIGH)
                    ispressedBT4 = False 
                    time.sleep(0.5)
                else: 
                    GPIO.output(LED, GPIO.LOW)
                    ispressedBT4 = False
                    time.sleep(0.5)
        if ispressedBT3: 
            print("Durring Blinking") 
            if GPIO.input(LED) == GPIO.LOW:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(1)
            if GPIO.input(LED) == GPIO.HIGH:
                GPIO.output(LED, GPIO.LOW)
                time.sleep(1)             

try:
    main()
except KeyboardInterrupt: 
    GPIO.cleanup() 