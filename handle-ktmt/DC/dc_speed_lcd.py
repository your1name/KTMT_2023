import RPi.GPIO as GPIO 
import time

LCD_RS = 23
LCD_E = 27 
LCD_D4 = 18 
LCD_D5 = 17 
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.00005
E_DELAY = 0.00005

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

def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20 
    BT4 = 19 
    DIR = 25
    PWD = 24
    GPIO.setmode(GPIO.BCM)

    lcd_init()
    GPIO.output(LED_ON, True)

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
            lcd_clear()
            lcd_string(str(currentPWD1))
            currentPWD2 = 0
            time.sleep(0.5)
        
        if GPIO.input(BT2) == 0:
            print("Press BT2") 
            PWD2.ChangeDutyCycle(0)
            downPWD = int(0.2 * currentPWD1)
            currentPWD1 = (currentPWD1 - downPWD) if currentPWD1 - downPWD > 0 else 0
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Toc do hien tai: " + str(currentPWD1) + " theo chieu thuan")
            lcd_clear()
            lcd_string(str(currentPWD1))
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
            lcd_clear()
            lcd_string(str(currentPWD2))
            currentPWD1 = 0
            time.sleep(0.5)
            
        if GPIO.input(BT4) == 0:
            print("Press BT4") 
            PWD1.ChangeDutyCycle(0)
            downPWD = int(20 / 100 * currentPWD2)
            currentPWD2 = (currentPWD2 - downPWD) if currentPWD2 - downPWD > 0 else 0
            print("Toc do hien tai: -" + str(currentPWD2))
            lcd_clear()
            lcd_string(str(currentPWD2))
            PWD2.ChangeDutyCycle(currentPWD2)
            currentPWD1 = 0
            time.sleep(0.5)


try:
    main()
except KeyboardInterrupt:
    PWD1.stop()
    PWD2.stop()
    lcd_clear()     

