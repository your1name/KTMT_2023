import cv2 
import copy
import numpy as np
import RPi.GPIO as GPIO
def main():
    BT1 = 21
    BT2 = 26
    # Mở camera
    cap = cv2.VideoCapture(0)
    print("Campture is ok")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    isdraw = False
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("press BT1")
            while True:
                ret, src = cap.read()
                frame = copy.copy(src) # tạo bản sao để trách tác động src
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # chuyển không gian HSV
                mask = cv2.inRange(hsv, (35,89,107),(45,241,213)) # tạo mask
                # Tìm coutour
                _, coutours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                result = cv2.bitwise_or(frame, frame, mask=mask) # mask với frame
                # --------BT2---------- Bấm nút về coutour
                if GPIO.input(BT2) == GPIO.LOW:
                    isdraw = True
                if isdraw:
                    draw(coutours, result)
                # ----------------
                cv2.imshow("Camera", src)
                cv2.imshow("Threshold", result)
                # Press q to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    GPIO.cleanup()
                    cv2.destroyAllWindows()
                    break
def nothing(x):
    pass
def draw(coutours, frame):
    if coutours is None:
        print("No have coutours. Please try to agian")
    for i in range(len(coutours)):
        if cv2.coutourArea(coutours[i]) > 300:
            hull = convexHull(coutours[i])
            cv2.drawContours(frame, [hull], -1, (0,255,0))
try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
	cv2.destroyAllWindows()

