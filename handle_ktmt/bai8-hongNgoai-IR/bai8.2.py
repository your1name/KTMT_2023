# hiển thị các ký tự nhận được từ điều khiển từ xa. Khi nhận được phím 8
# trên điều khiển sẽ bật role 1, số 9 bật role 2 

import RPi.GPIO as GPIO
import time

def main():
    PIN = 22
    rl_1 = 16
    rl_2 = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rl_1, GPIO.OUT)
    GPIO.setup(rl_2, GPIO.OUT)
    GPIO.output(rl_1, False)
    GPIO.output(rl_2, True)

    # setup IR pin as input
    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
    print('irm test start....')
    BUTTON8 = False

    while True:
        reader = read_IRM(PIN) 
        
        if reader == 'button 8':
            if not BUTTON8:
                GPIO.output(rl_1, True)
                BUTTON8 = True
                print(BUTTON8)
                time.sleep(0.2)
            else:
                GPIO.output(rl_1, False)
                BUTTON8 = False
                print(BUTTON8)
                time.sleep(0.2)

        if reader == 'button 9':
            GPIO.output(rl_2, False)
        time.sleep(0.2)


def read_IRM(PIN):
    while True:
        if GPIO.input(PIN) == 0:
            count = 0
            while GPIO.input(PIN) == 0 and count < 200:
                count += 1
                time.sleep(0.00006)
            count = 0
            while GPIO.input(PIN) == 1 and count < 80:
                count += 1
                time.sleep(0.00006)
            idx = 0
            cnt = 0
            data = [0, 0, 0, 0]
            for i in range(0,32):
                count = 0
                while GPIO.input(PIN) == 0 and count < 15:
                    count += 1
                    time.sleep(0.00006)
                    count = 0
                while GPIO.input(PIN) == 1 and count < 40:
                    count += 1
                    time.sleep(0.00006)
                if count > 8:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:
                print('get key 0x%02x' %data[2])
                print(exec_cmd(data[2]))
                return exec_cmd(data[2])

def exec_cmd(key_val):
    if (key_val == 0x45):
        return "button CH-"
    elif (key_val == 0x46):
        return "button CH"
    elif (key_val == 0x47):
        return "button CH+"
    elif (key_val == 0x44):
        return "button PREV"
    elif (key_val == 0x40):
        return "button NEXT"
    elif (key_val == 0x43):
        return "button PLAY/PAUSE"
    elif (key_val == 0x07):
        return "button VOL-"
    elif (key_val == 0x15):
        return "button VOL+"
    elif (key_val == 0x09):
        return "button EQ"
    elif (key_val == 0x16):
        return "button 0"
    elif (key_val == 0x19):
        return "button 100+"
    elif (key_val == 0x0d):
        return "button 200+"
    elif (key_val == 0x0c):
        return "button 1"
    elif (key_val == 0x18):
        return "button 2"
    elif (key_val == 0x5e):
        return "button 3"
    elif (key_val == 0x08):
        return "button 4"
    elif (key_val == 0x1c):
        return "button 5"
    elif (key_val == 0x5a):
        return "button 6"
    elif (key_val == 0x42):
        return "button 7"
    elif (key_val == 0x52):
        return "button 8"
    elif (key_val == 0x4a):
        return "button 9"
    
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()