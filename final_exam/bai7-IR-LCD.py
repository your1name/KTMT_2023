
# Viết chương trình giải mã tín hiệu điều khiển từ xa từ điều khiển hồng ngoại
# hiển thị LCD
import RPi.GPIO as GPIO
import time

# Define GPIO cho LCD
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
    # defirne IR pin
    PIN = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
    
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)

    print('im test start...')
    while True:
        reader = read_IRM(PIN) # reader is String
        # lcd_clear()
        lcd_string(reader)
        time.sleep(1)




def read_IRM(PIN):
    while True:
        if GPIO.input(PIN) == 0:
            count = 0
            while GPIO.input(PIN) == 0 and count < 200:
                count += 1
                time.sleep(0.00006)
            count = 0
            while GPIO.input(PIN) == 1 and count < 80:
                count += 1
                time.sleep(0.00006)
            idx = 0
            cnt = 0
            data = [0, 0, 0, 0]
            for i in range(0,32):
                count = 0
                while GPIO.input(PIN) == 0 and count < 15:
                    count += 1
                    time.sleep(0.00006)
                    count = 0
                while GPIO.input(PIN) == 1 and count < 40:
                    count += 1
                    time.sleep(0.00006)
                if count > 8:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:
                print('get key 0x%02x' %data[2])
                print(exec_cmd(data[2]))
                return exec_cmd(data[2])

def exec_cmd(key_val):
    if (key_val == 0x45):
        return "button CH-"
    elif (key_val == 0x46):
        return "button CH"
    elif (key_val == 0x47):
        return "button CH+"
    elif (key_val == 0x44):
        return "button PREV"
    elif (key_val == 0x40):
        return "button NEXT"
    elif (key_val == 0x43):
        return "button PLAY/PAUSE"
    elif (key_val == 0x07):
        return "button VOL-"
    elif (key_val == 0x15):
        return "button VOL+"
    elif (key_val == 0x09):
        return "button EQ"
    elif (key_val == 0x16):
        return "button 0"
    elif (key_val == 0x19):
        return "button 100+"
    elif (key_val == 0x0d):
        return "button 200+"
    elif (key_val == 0x0c):
        return "button 1"
    elif (key_val == 0x18):
        return "button 2"
    elif (key_val == 0x5e):
        return "button 3"
    elif (key_val == 0x08):
        return "button 4"
    elif (key_val == 0x1c):
        return "button 5"
    elif (key_val == 0x5a):
        return "button 6"
    elif (key_val == 0x42):
        return "button 7"
    elif (key_val == 0x52):
        return "button 8"
    elif (key_val == 0x4a):
        return "button 9"

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
    GPIO.cleanup()