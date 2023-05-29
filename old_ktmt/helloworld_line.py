# Viết chương trình vẽ đường thẳng gạch dưới chữ hello world hiển thị lên glcd
# bấm bt1 xoá dòng chữ vừa hiện
import time
import RPi.GPIO as GPIO
import Adafruit_Nokia_LCD as LCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    BT1 = 14
    SCLK = 23
    DIN = 27
    DC = 17
    RST = 15
    CS = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global disp
    disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
    disp.begin(contrast=60)
    disp.clear()
    disp.display()
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    # draw.rectangle((0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
    #                outline=0, fill=100)
    font = ImageFont.load_default()
    draw.text((10, 10), 'Hello World', font=font)  # chen chu
    draw.line((10, 20, 74, 20), fill=0)  # mo
    # hien thi hinh anh
    disp.image(image)
    disp.display()
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            disp.clear()
            disp.display()
        time.sleep(2)


try:
    main()
except KeyboardInterrupt:
    disp.clear()
