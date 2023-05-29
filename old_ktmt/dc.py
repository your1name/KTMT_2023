# Viết chương trình mỗi lần bấm BT1, động cơ DC tăng tốc độ lên 10%\
# hiển thị tốc độ lên màn hình GLCD
import RPi.GPIO as GPIO
from config import Config
import time


def main():
    BT1 = 14
    DIR = 19
    PWD = 13
    GPIO.setmode(GPIO.BCM)
    # Khoi tao va pull up cac nut bam
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Khoi tao dong co DC
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2           # Khoi tao cac bien global
    PWD1 = GPIO.PWM(DIR, 100)   # Tan so 100Hz
    PWD2 = GPIO.PWM(PWD, 100)   # Tan so 100HZ
    PWD1.start(0)   # Khoi dong
    PWD2.start(0)   # Khoi dong
    currentPWD1 = 20  # Toc do hien tai cua PWD1
    currentPWD2 = 20  # Toc do hien tai cua PWD2
    print("Chuan bi hoan tat ok")
    while True:
        # Duty Cycle la chu ky nhiem
        # Chu ky nhiem la phan tram thoi gian giua cac xung
        # ma tin hieu o muc "high" hoac "ON"
        # Tang toc va chay theo chieu kim dong ho
        if GPIO.input(BT1) == GPIO.LOW:
            print("Press BT1")
            PWD2.ChangeDutyCycle(0)
            time.sleep(1)
            upPWD = 10
            currentPWD1 = (currentPWD1 + upPWD) if currentPWD1 < 100 else 100
            # Thay doi toc do theo bien currentPWD1
            handleDutyCycle(PWD1, currentPWD1, currentPWD2)
            print("Toc do hien tai: " + str(currentPWD1) + " theo chieu thuan")
            currentPWD2 = 0
            time.sleep(0.5)


def handleDutyCycle(PWD, currentPWD, currentPWDpre):
    print(currentPWDpre)
    if currentPWD > 100 or currentPWD < 0:
        print("Khong the tang hay giam toc nua")
        return
    # neu DC dang chay nguoc chieu thi dung mot luc de tranh su co
    elif currentPWDpre != 0:
        time.sleep(1)
    PWD.ChangeDutyCycle(currentPWD)


try:
    main()
except KeyboardInterrupt:
    # Dung cac dong co va giai phong GPIO
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()
