import time
import RPi.GPIO as GPIO

def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    BT4 = 19
    DIR = 25
    PWD = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # khoi tao dong co DC
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2 # khoi tao bien global
    PWD1 = GPIO.PWM(DIR, 100) # tan so 100Hz
    PWD2 = GPIO.PWM(PWD, 100) # tan so 100Hz
    PWD1.start(0) # khoi dong
    PWD2.start(0) # khoi dong
    currentPWD1 = 20 # toc do hien tai cua PWD1
    currentPWD2 = 20 # toc do hien tai cua PWD2
    print("Chuẩn bị hoàn tất: ok")
    while True:
        # Tăng tốc và chạy theo chiều kim đồng hồ
        if GPIO.input(BT1) == 0:
            print("Press BT1")
            if currentPWD2 != 0:
                PWD2.ChangeDutyCycle(0)
                time.sleep(1)
                upPWD = int(0.2 * currentPWD1)
                currentPWD1 = (currentPWD1 + upPWD) if currentPWD1 + upPWD < 100 else 100
                if currentPWD1 == 0:
                    currentPWD1 = 20
                # thay đổi tốc độ theo biến currentPWD1
                PWD1.ChangeDutyCycle(currentPWD1)
                print("Tốc độ hiện tại: "+str(currentPWD1)+" theo chiều thuận")
                currentPWD2 = 0
                time.sleep(0.5)
        # giảm tốc và chay theo chiều kim đồng hồ
        if GPIO.input(BT2) == 0:
            print("Press BT2")
            PWD2.ChangeDutyCycle(0)
            downPWD = int(0.2 *currentPWD1)
            currentPWD1 = (currentPWD1 - downPWD) if currentPWD1 - downPWD > 0 else 0
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Tốc độ hiện tại: "+str(currentPWD1)+" theo chiều thuận")
            currentPWD2 = 0
            time.sleep(0.5)
            
        # tăng tốc và chay theo ngược kim đồng hồ
        if GPIO.input(BT3) == 0:
            print("Press BT3")
            if currentPWD1 != 0:
                PWD1.ChangeDutyCycle(0)
                time.sleep(1)
                upPWD = int(20/100 * currentPWD2)
                currentPWD2 = (currentPWD2 + upPWD) if currentPWD2 + upPWD < 100 else 100
                if currentPWD2 == 0:
                    currentPWD2= 20
                # thay đổi tốc độ theo biến currentPWD1
                PWD2.ChangeDutyCycle(currentPWD2)
                print("Tốc độ hiện tại: "+str(currentPWD2)+" theo chiều thuận")
                currentPWD1 = 0
                time.sleep(0.5)
        # giảm tốc và chay theo ngược kim đồng hồ
        if GPIO.input(BT4) == 0:
            print("Press BT4")
            PWD1.ChangeDutyCycle(0)
            downPWD = int(20/100 *currentPWD2)
            currentPWD2 = (currentPWD2 - downPWD) if currentPWD2 - downPWD > 0 else 0
            PWD2.ChangeDutyCycle(currentPWD2)
            print("Tốc độ hiện tại: "+str(currentPWD2)+" theo chiều thuận")
            currentPWD1 = 0
            time.sleep(0.5)
                
try:
    main()
except KeyboardInterrupt:
    # dừng các động cơ và giải phóng GPIO
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()





   