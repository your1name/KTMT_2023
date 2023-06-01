import re
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

def main(cascaded, block_orentation, rotate):
    # create matrix device
    serial = spi(port =0, device = 0, gpio=noop())
    device = max7219(serial, cascaded=cascaded,block_orentation=block_orentation, rotate = rotate)
    device.contrast(20)

    # debugging purpose
    print("[-] Matrix initialized")
    #print hello world on the matrix display
    msg = "0123456789"
    # debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill = "white", font = proportional(CP437_FONT),scroll_delay=0.1)

if __name__ == "__main__":
    # cascaded = Number of cascaded MAX7219 LED matrices default=1
    # block_orientation = choices 0, 90, -90 corrects block orientation, default=0
    # retate = choices 0, 1, 2, 3, Rotate display

    try:
        main(cascaded=1, block_orentation=0,rotate=0)
    except KeyboardInterrupt:
        pass


