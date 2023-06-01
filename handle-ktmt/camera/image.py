import cv2
import RPi.GPIO as GPIO 
import time

def main():
    BT1 = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(0) # khoi dong camera
    print("Capture da ok")
    while True:
        ret, frame = capture.read() # doc video tu camera
        # frame duoc tra ve la dang ma tran; numpy.array print(type(frame))
        # chieu dai va chieu rong la co cua ma tran, print(frame.shape)
        if GPIO.input(BT1) == GPIO.LOW:
            while True:
                # hien hinh anh ra man hinh tu bien frame 
                # cv2.imshow se doc frame, chuyen frame ra dang anh 
                cv2.imshow("Anh chup camera", frame)
                cv2.waitKey()
                cv2.destroyWindow("Anh chup camera")
                break

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(namewindow)