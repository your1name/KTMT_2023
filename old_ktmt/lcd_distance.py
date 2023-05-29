# Viết chương trình đọc giá trị cảm biến siêu âm, hiển thị giá trị khoảng cách lên glcd

import RPi.GPIO as GPIO
import time
import Adafruit_Nokia_LCD as LCD
from PIL import Image, ImageDraw, ImageFont


def main():
    # GPIO pins
    TRIG = 16
    ECHO = 26
    global pulse_end
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    while True:
        print('waiting for sensor to settle')
        time.sleep(2)
        # bat, tat song sieu am
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        # tinh thoi gian
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
        # tinh k/c
        dist = (pulse_end-pulse_start)*17150
        dist = round(dist, 2)
        lcd(dist)


def lcd(distance):
    SCLK = 23
    DIN = 27
    DC = 17
    RST = 15
    CS = 18
    global disp  # khoi tao bien global
    disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)  # khoi tao LCD
    disp.begin(contrast=60)  # cai dat do sang
    disp.clear()
    disp.display()
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    # draw.rectangle((0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
    #                outline=0, fill=100)
    font = ImageFont.load_default()
    draw.text((30, 15), str(distance), font=font)  # chen chu
    disp.image(image)
    disp.display()


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
