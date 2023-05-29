# Viết chương trình mỗi lần bấm BT1, động cơ DC tăng tốc độ lên 10%\
# hiển thị tốc độ lên màn hình GLCD
import RPi.GPIO as GPIO
import time


#Define GPIO cho LCD
# Define GPIO cho LCD
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
# Define some divice constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.00005
E_DELAY = 0.00005


def main():
    BT1 = 14
    DIR = 19
    PWD = 13
    GPIO.setmode(GPIO.BCM)

    # khởi tạo LCD
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)


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

        lcd_string(str(currentPWD1))
 

def handleDutyCycle(PWD, currentPWD, currentPWDpre):
    print(currentPWDpre)
    if currentPWD > 100 or currentPWD < 0:
        print("Khong the tang hay giam toc nua")
        return
    # neu DC dang chay nguoc chieu thi dung mot luc de tranh su co
    elif currentPWDpre != 0:
        time.sleep(1)
    PWD.ChangeDutyCycle(currentPWD)

def lcd_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)
    GPIO.setup(LED_ON, GPIO.OUT)
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)

def lcd_string(message):
    lcd_byte(LCD_LINE_1, False)
    for i in range(len(message)):
        lcd_byte(ord(message[i]), LCD_CHR)

def lcd_clear():
    lcd_string("            ")

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


try:
    main()
except KeyboardInterrupt:
    # Dung cac dong co va giai phong GPIO
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()
