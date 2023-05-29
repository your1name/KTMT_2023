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

def main():
    lcd_init()
    # Toggle backlight on-off-on
    GPIO.output(LED_ON, True)
    time.sleep(1)
    GPIO.output(LED_ON, False)
    time.sleep(1)
    # Send some centred test
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Rasbperry Pi", 2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("KTMT", 2)
    time.sleep(3) # 3 second delay
    # Send some left justified text
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("thay Thao dep giai", 1)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(":))", 1)
    time.sleep(3) # 3 second delay
    # Send some left justified text
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Hello world", 3)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("abc...xyz", 3)

    time.sleep(30) 
    # Turn off backlight
    GPIO.output(LED_ON, False)

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
    #Initalise display
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)

def lcd_string(message, style):
    # Send string to display
    # Style = 1 Left justified
    # style = 2 Centred
    # style = 3 Right justified
    if style == 1:
        message = message.ljust(LCD_WIDTH," ")
    elif style ==2:
        message = message.center(LCD_WIDTH, " ")
    elif style == 3:
        message = message.rjust(LCD_WIDTH," ")
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

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

main()




    


    
   










