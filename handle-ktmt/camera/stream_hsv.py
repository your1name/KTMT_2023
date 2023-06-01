import cv2
import copy
import RPi.GPIO as GPIO

def nothing(x):
	pass

def main():
	BT1 = 21
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	cap = cv2.VideoCapture(0)
	print("Capture ok")
	# create a window
	while True:
		if GPIO.input(BT1) == GPIO.LOW:
			print("BT1 pressed")
			cv2.namedWindow('image')
			# tao cac thanh slider de chinh nguong mau
			cv2.createTrackbar('lowH', 'image', 0, 180, nothing)
			cv2.createTrackbar('highH', 'image', 179, 180, nothing)
			cv2.createTrackbar('lowS', 'image', 0, 255, nothing)
			cv2.createTrackbar('highS', 'image', 255, 255, nothing)
			cv2.createTrackbar('lowV', 'image', 0, 255, nothing)
			cv2.createTrackbar('highV', 'image', 255, 255, nothing)
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(CBT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			while True:
				_, src = cap.read()
				# dat vi tri tren slider
				ilowH = cv2.getTrackbarPos('lowH', 'image')
				ihighH = cv2.getTrackbarPos('highH', 'image')
				ilowS = cv2.getTrackbarPos('lowS', 'image')
				ihighS = cv2.getTrackbarPos('highS', 'image')
				ilowV = cv2.getTrackbarPos('lowV', 'image')
				ihighV = cv2.getTrackbarPos('highV', 'image')
				hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) # chuyen sang khong gian HSV
				# phan nguong trong khong gian HSV
				mask = cv2.inRange(hsv, (ilowH, ilowS, ilowV), (ihighH, ihighS, ihighV))
				# su dung mask de loc mau voi anh goc
				result = cv2.bitwise_or(src, src, mask=mask)
				cv2.imshow('image', result)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					GPIO.cleanup()
					break

try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
	cv2.destroyAllWindows()