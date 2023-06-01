from multiprocessing import Process, Value
import RPi.GPIO as GPIO
import time


# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


def lcd_init():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    GPIO.setup(LED_ON, GPIO.OUT)  # Backlight enable
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)


def lcd_string(message, position, line):
    message = message.rjust(len(message) + position)
    if line == 1:
        lcd_byte(LCD_LINE_1, False)
    else:
        lcd_byte(LCD_LINE_2, False)
    for i in range(len(message)):
        lcd_byte(ord(message[i]), LCD_CHR)


def lcd_clear():
    lcd_string("                ", 0, 1)
    lcd_string("                ", 0, 2)


# Very headache function
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    GPIO.output(LCD_RS, mode)  # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def replacer(s, newstring, index):
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


def reader(BT2, r_to_l):
    while True:
        if GPIO.input(BT2) == 0:
            if r_to_l.value:
                r_to_l.value = False
            else:
                r_to_l.value = True
        time.sleep(0.2)


def main():
    GPIO.setmode(GPIO.BCM)
    BT1 = 21
    BT2 = 26

    # Setup for button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, GPIO.PUD_UP)
    # Set up for LCD
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)

    while GPIO.input(BT1) != 0:
        pass

    hello = "     hello-world"
    print(hello)
    lcd_string(hello, 0, 1)

    # wait for button 2 to run the hello-world thing...
    while GPIO.input(BT2) != 0:
        pass

    r_to_l = Value('i', True)
    Process(target=reader, args=(BT2, r_to_l)).start()
    while True:
        if r_to_l.value:
            i = 0
            while hello[i] != " ":
                i += 1
                if i == len(hello):
                    break
            while hello[i] == " ":
                i += 1
                if i == len(hello):
                    break
            if i != 0 and i != len(hello):
                tmp = hello[i - 1]
                hello = replacer(hello, hello[i], i - 1)
                hello = replacer(hello, tmp, i)
        else:
            i = len(hello) - 1
            while hello[i] != " ":
                i -= 1
                if i == -1:
                    break
            while hello[i] == " ":
                i -= 1
                if i == -1:
                    break
            if i != -1:
                tmp = hello[i + 1]
                hello = replacer(hello, hello[i], i + 1)
                hello = replacer(hello, tmp, i)
        lcd_clear()
        lcd_string(hello, 0, 1)
        time.sleep(0.2)


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
