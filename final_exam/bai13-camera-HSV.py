# Viết chương trình hiển thị các thanh trượt điều chỉnh cường độ
# trong không gian màu HSV để điều chỉnh ảnh từ camera
import cv2
import RPi.GPIO as GPIO


def nothing(x):
    pass


def main():
    BT1 = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    cap = cv2.VideoCapture(0)
    print("Cap ok")
    # Create a window
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("Press BT1")
            cv2.namedWindow('image')
            # thạo các thanh slider để chỉnh ngưỡng màu
            cv2.createTrackbar('lowH', 'image', 0, 180, nothing)
            cv2.createTrackbar('highH', 'image', 179, 180, nothing)
            cv2.createTrackbar('lowS', 'image', 0, 255, nothing)
            cv2.createTrackbar('highS', 'image', 255, 255, nothing)
            cv2.createTrackbar('lowV', 'image', 0, 255, nothing)
            cv2.createTrackbar('highV', 'image', 255, 255, nothing)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            while True:
                _, src = cap.read()
                # đặt vị trí trên slider
                ilowH = cv2.getTrackbarPos('lowH', 'image')
                ihighH = cv2.getTrackbarPos('highH', 'image')
                ilowS = cv2.getTrackbarPos('lowS', 'image')
                ihighS = cv2.getTrackbarPos('highS', 'image')
                ilowV = cv2. getTrackbarPos('lowV', 'image')
                ihighV = cv2.getTrackbarPos('highV', 'image')
                # chuyển sang không gian HSV
                hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
                # ! Phân nguồng trong không gian HSV
                mask = cv2.inRange(hsv, (ilowH, ilowS, ilowV),
                                   (ihighH, ihighS, ihighV))
                # sử dụng mask để lọc màu với ảnh gốc
                result = cv2.bitwise_or(src, src, mask=mask)
                cv2.imshow('image', result)
                # Press q to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    GPIO.cleanup()
                    break


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllwindows()
