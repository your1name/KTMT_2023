import cv2
import RPi.GPIO as GPIO
import time

def main():
    BT4 = 19
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(0) # khoi dong camera
    print("Capture đã ok")
    cap_stream = False
    while capture.isOpened(): # neu camera mo
        ret, frame = capture.read() # doc video tu camera
        if GPIO.input(BT4) == GPIO.LOW:
            print("press BT4")
            if not cap_stream:
                cap_stream = True
                time.sleep(0.5)
                continue
            if cap_stream:
                cap_stream = False
                cv2.destroyAllWindows(namewindow)
                time.sleep(0.5)
                continue
        if cap_stream:
            cv2.imshow(namewindow, frame)
        # -------------------
        if cv2.waitKey(1) & 0xFF == ord('q'): # bam q de thoat
            GPIO.cleanup()
            cv2.destroyWindow()
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(namewindow)
 

 