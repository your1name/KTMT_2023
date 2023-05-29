# For Led
LED = 13
BT1 = 21
BT2 = 26
BT3 = 20
BT4 = 19
rl_1 = 16
rl_2 = 12

# For LCD
```python

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

    # GPIO.setmode(GPIO.BCM)
    
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)


```

# For Led Matrix

Install

```bash
git clone https://github.com/diy-hus/max7219
python3 -m pip install --upgrade luma.led_matrix 
```
Uninstall
```bash
python3 -m pip uninstall --upgrade luma.led_matrix 
```

Code [Example](./final_exam/bai3-BT-Led.py)

# For Camera
Install
```bash
https://github.com/diy-hus/opencv
cd opencv
pip3 install opencv_python-3.4.13.47-cp37-cp37m-linux_armv7l.whl

# if error
sudo apt-get install libatlas-base-dev
```

Uninstall
```bash
sudo apt-get install libatlas-base-dev
```

