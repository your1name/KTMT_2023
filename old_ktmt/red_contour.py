# Viết chương trình bấm BT1, chụp ảnh và khoanh vùng những vật có màu đỏ, hiện ảnh lên màn hình
import cv2
import copy
import numpy as np
import RPi.GPIO as GPIO


def main():
    BT1 = 14
    # Mở camera
    cap = cv2.VideoCapture(0)
    print("Capture is ok")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        if GPIO.input(BT1) == GPIO. LOW:
            print("Presa BT1")
            while True:
                ret, src = cap.read()
                frame = copy.copy(src)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                red_mask = cv2.inRange(hsv, (35, 89, 107), (45, 241, 213))
                # Tim contour
                _, contours, _ = cv2.findContours(
                    red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                result = cv2.bitwise_or(frame, frame, mask=red_mask)

                if GPIO.input(BT1) == GPIO.LOW:
                    draw(contours, result)

                    cv2.imshow("Camera", src)
                    cv2.imshow('Threshold', result)
                    # Press q to exit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        GPIO.cleanup()
                        cv2.destroyAllWindows()
                        break


def nothing(x):
    pass


def draw(contours, frame):
    if contours is None:
        print("No have contours. Plasse try to agian")
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 300:
            hull = cv2.convexHull(contours[i])
            cv2.drawContours(frame, [hull], -1, (0, 255, 0))


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()
