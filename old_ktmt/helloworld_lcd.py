# Viết chương trình bấm BT1 hiển thị hello-world ra terminal, ra màn hình lcd
import RPi.GPIO as GPIO
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_Nokia_LCD as LCD


def main():
    # message for print out
    msg = '*hello-world'
    # GPIO pins
    BT1 = 14
    SCLK = 23
    DIN = 27
    DC = 17
    RST = 15
    CS = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # init LCD
    global disp
    disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
    disp.begin(contrast=60)
    disp.clear()
    disp.display()
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))  # create new image
    draw = ImageDraw.Draw(image)
    # draw.rectangle((0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
    #                outline=0, fill=100)
    font = ImageFont.load_default()
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            # print out the message on LCD
            draw.text((8, 30), msg, font=font)
            disp.image(image)
            disp.display()
            # print out the message on terminal
            print(msg)
            time.sleep(1)


try:
    main()
except KeyboardInterrupt:
    disp.clear()
