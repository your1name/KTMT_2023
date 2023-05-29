
# GPIO event detectcho phép chúng ta tạo một hàm 
# được gọi mỗi khi có sự thay đổi trạng thái của nút nhấn, 
# mà không cần kiểm tra trạng thái của nút nhấn trong vòng lặp chính

# LED nhấp nháy, bấm BT1 dừng hoặc tiếp tục nháy
import RPi.GPIO as GPIO
import time

ispressBT1 = False
LED = 13



# Định nghĩa các callback
def bt1_callback(channel):
    global ispressBT1
    print("BT1 press")
    if not ispressBT1:
        ispressBT1 = True
        GPIO.output(LED, GPIO.LOW)
    else:
        ispressBT1 = False



def main():
    BT1 = 21

    GPIO.setmode(GPIO.BCM)  # setup mode

    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED, GPIO.OUT)

    # Đặt hàm callback cho nút nhấn với sự kiện cả RISING và FALLING or BOTH
    GPIO.add_event_detect(BT1, GPIO.FALLING, callback = bt1_callback, bouncetime=300) 
    # 300ms
    global ispressBT1
    while True:
        if not ispressBT1:
            print("During Blinking")
            if GPIO.input(LED) == GPIO.LOW:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(1)
            else:
                GPIO.output(LED, GPIO.LOW)
                time.sleep(1)
        


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    main()

