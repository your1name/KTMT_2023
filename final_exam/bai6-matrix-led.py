
import re
import RPi.GPIO as GPIO
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

ispressBT2 = False
ispressBT3 = False
ispressBT4 = False


def bt2_callback(channel):
    global ispressBT2
    global ispressBT3
    print("BT2 press")
    if ispressBT3:
        ispressBT2 = True


def bt3_callback(channel):
    global ispressBT3
    print("BT3 press")
    ispressBT3 = True
    
def bt4_callback(channel):
    global ispressBT2
    global ispressBT3
    global ispressBT4

    print("BT4 press")

    if ispressBT3 and ispressBT2 :
        ispressBT4 = True


def main(cascaded, block_orentation, rotate):
    BT2 = 26
    BT3 = 20
    BT4 = 19

    DIR = 25
    PWD = 24

    rl_1 = 16

    

    GPIO.setmode(GPIO.BCM)  # setup mode
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    GPIO.add_event_detect(BT2, GPIO.FALLING, callback = bt2_callback, bouncetime=300) 
    GPIO.add_event_detect(BT3, GPIO.FALLING, callback = bt3_callback, bouncetime=300) 
    GPIO.add_event_detect(BT4, GPIO.FALLING, callback = bt4_callback, bouncetime=300)
    # 300ms
    global ispressBT1
    global ispressBT2
    global ispressBT3
    global ispressBT4

    # khoi tao dc
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2
    PWD1 = GPIO.PWM(DIR,100)
    PWD2 = GPIO.PWM(PWD,100)
 
   

    #   khoi tao role
    GPIO.setup(rl_1,GPIO.OUT)
    GPIO.output(rl_1, False)

    # create matrix device
    serial = spi(port =0, device = 0, gpio=noop())
    device = max7219(serial, cascaded=cascaded,block_orentation=block_orentation, rotate = rotate)
    device.contrast(20)

    # debugging purpose
    

    print("[-] Matrix initialized")
    #print hello world on the matrix display
    for i in range(9,-1,-1):
        msg = str(i)
        # debugging purpose
        print("[-] Printing: %s" % msg)
        
        time.sleep(0.1)
 
        # show_message(device, msg, fill = "white", font = proportional(CP437_FONT),scroll_delay=None)
        show_message(device, msg, fill = "white", font = proportional(CP437_FONT),scroll_delay=0.1)

        if ispressBT2 and ispressBT3 and ispressBT4:
            while True:
                show_message(device, msg, fill = "white", font = proportional(CP437_FONT))

        if i == 0:
            GPIO.output(rl_1, True)
            PWD1.start(20)
            PWD2.start(0)

            show_message(device, "Hello World", fill = "white", font = proportional(CP437_FONT),scroll_delay=0.1)


            



if __name__ == "__main__":
    # cascaded = Number of cascaded MAX7219 LED matrices default=1
    # block_orientation = choices 0, 90, -90 corrects block orientation, default=0
    # retate = choices 0, 1, 2, 3, Rotate display
    
    # 0 = up -> down
    # 1 = right -> left
    # 2 = down -> up
    # 3 = left -> right
    try:
        main(cascaded=1, block_orentation=0,rotate=1)
    except KeyboardInterrupt:
        PWD1.stop()
        PWD2.stop()
        GPIO.cleanup()


