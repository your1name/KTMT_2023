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
# Define some divice constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # 1 LCD RAM add
LCD_LINE_2 = 0xC0 # 2 LCD RAM add
#Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

# bt1 
BT1 = 21
def lcd_init():
    GPIO.setmode(GPIO.BCM) # uses BCM GPIO numbers
    GPIO.setwarnings(False) 
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5        
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # backlight enabls
    #Initalise display
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
    lcd_string("             ", 0,1)
    lcd_string("             ",0, 2)

# Very headache function
def lcd_byte(bits, mode):
    # Send byte to data point
    # bits = data
    # mode = True for character
    #        False for conmand
    GPIO.output(LCD_RS, mode) # RS
    # High bits
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
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    # low bits
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

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, GPIO.PUD_UP)
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)

    mode = 2
    position = 0
    while True:
        if GPIO.input(BT1) == 0:
            mode += 1
        if mode ==3:
            mode = 0

        if mode == 0 and position  < 5:
            position += 1
            lcd_clear()
            lcd_string("Hello-World", position, 1)
        if mode == 1 and position > 0:
            position -= 1
            lcd_clear()
            lcd_string("Hello-World", position, 1)

        if mode == 2:
            lcd_clear()
            position = 0

        time.sleep(0.5)
main()

