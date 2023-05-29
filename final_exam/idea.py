# viết chương trình hiển thị hello world ra màn hình, từng ký tự một chạy từ trái sang phải terminal

# import RPi.GPIO as GPIO
import time


def main():
    msg = '*hello world'
    msg1 = msg
    rangee = 30
    for k in range(len(msg)+1):
        if k >= 1:
            lPart = msg[:-k]
            runChar = msg[-k]
            for i in range(rangee):
                msg1 = lPart + ' '*i + runChar
                print(msg1, end='\r')
                time.sleep(0.02)
        else:
            print(msg1, end='\r')
            time.sleep(0.02)


try:
    main()
except KeyboardInterrupt:
    # GPIO.cleanup()
    print()
