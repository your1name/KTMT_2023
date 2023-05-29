# Viết chương trình vẽ hình tròn, tâm ở chính giữa, đường kính 30pixel và hiển thị lên GLCD
import RPi.GPIO as GPIO
import Adafruit_Nokia_LCD as LCD
from PIL import Image, ImageDraw


def main():
    radius = 15
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
    draw.rectangle((0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                   outline=0, fill=255)
    x = (LCD.LCDWIDTH-1)/2
    y = (LCD.LCDHEIGHT-1)/2
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline=0, fill=255)
    disp.image(image)
    disp.display()


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
