import cv2
import RPi.GPIO as GPIO
import time
def main():
    BT2 = 26
    BT3 = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    global nameWindow
    nameWindow = 'Camera user'

    capture = cv2.VideoCapture(0) # khoi dong camera
    print('capture da ok')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # dinh dang cho viec quay vid
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20.0, (640,480))
    cap_video = False
    while True:
        ret, frame = capture.read()
        if GPIO.input(BT2) == GPIO.LOW:
            print('press bt2')
            cv2.imshow(nameWindow,frame)
            out.write(frame)
            print('luu video')
            if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to exit
                GPIO.cleanup()
                cv2.destroyWindow(nameWindow)
                break
            continue
        if GPIO.input(BT3) == GPIO.LOW:
            print('press bt3')
            if cap_video:
                cap_video = False
                cv2.destroyWindow(nameWindow)
                continue
            time.sleep(0.5)
            if not cap_video:
                cap_video = True
                continue
        if cap_video:
            cv2.imshow(nameWindow, frame)
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to exit
            GPIO.cleanup()
            cv2.destroyWindow(nameWindow)
            break

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(nameWindow)
