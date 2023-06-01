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
    GPIO.output(rl_2, False)
    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
    print("irm test start...")
    while True:
        reader = read_IRM(PIN)
        if reader == "Button 8":
            GPIO.output(rl_1, True)
        if reader == "Button 9":
            GPIO.output(rl_2, True)
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
            for i in range(0, 32):
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
                print("Get the key: 0x%02x" % data[2])
                print(exec_cmd(data[2]))
                return exec_cmd(data[2])

def exec_cmd(key_val):
    if key_val == 0x45:
        return "Button CH-"
    elif key_val == 0x46:
        return "Button CH"
    elif key_val == 0x47:
        return "Button CH+"
    elif key_val == 0x44:
        return "Button PREV"
    elif key_val == 0x40:
        return "Button NEXT"
    elif key_val == 0x43:
        return "Button PLAY/PAUSE"
    elif key_val == 0x07:
        return "Button VOL-"
    elif key_val == 0x15:
        return "Button VOL+"
    elif key_val == 0x09:
        return "Button EQ"
    elif key_val == 0x16:
        return "Button 0"
    elif key_val == 0x19:
        return "Button 100+"
    elif key_val == 0x0d:
        return "Button 200+"
    elif key_val == 0x0c:
        return "Button 1"
    elif key_val == 0x18:
        return "Button 2"
    elif key_val == 0x5e:
        return "Button 3"
    elif key_val == 0x08:
        return "Button 4"
    elif key_val == 0x1c:
        return "Button 5"
    elif key_val == 0x5a:
        return "Button 6"
    elif key_val == 0x42:
        return "Button 7"
    elif key_val == 0x52:
        return "Button 8"
    elif key_val == 0x4a:
        return "Button 9"
    
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
