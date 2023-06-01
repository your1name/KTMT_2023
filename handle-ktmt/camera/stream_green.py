import cv2
import copy
import RPi.GPIO as GPIO

def main():
	BT1 = 21
	BT2 = 26
	cap = cv2.VideoCapture(0)
	print("Capture ok")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	isdraw = False
	while True:
		if GPIO.input(BT1) == GPIO.LOW:
			print("BT1 pressed")
			while True:
				ret, src = cap.read()
				frame = copy.copy(src)
				hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
				green_mask = cv2.inRange(hsv, (35, 89, 107), (45, 241, 213))
				_, contoursGreen, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
				red_mask = cv2.inRange(hsv, (0, 118, 130), (5, 255, 255))
				_, contoursRed, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
				# hop xanh va do lai
				# nhom mask xanh va do lai bang phep cong ma tran
				group = green_mask + red_mask
				# cac phan tu trong ma tran (Lon >= 1 la True va nguoc lai)
				group = group >= 1
				# tu kieu bool chuyen sang kieu uint8, nhan voi 255 de maskgroup co mau trang
				group = group.astype('uint8') * 255
				result = cv2.bitwise_or(frame, frame, mask=group)
				#----------------BT2----------------
				if GPIO.input(BT2) == GPIO.LOW:
					isdraw = True
				if isdraw:
					draw(contoursRed, contoursGreen, result)
				#-----------------------------------
				cv2.imshow("Threshold", result)
				cv2.imshow('Camera', src)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					GPIO.cleanup()
					cv2.destroyAllWindows()
					break

def nothing(x):
	pass

def draw(contoursRed, contoursGreen, frame):
	for i in range(len(contoursRed)):
		if cv2.contourArea(contoursRed[i]) > 300:
			hull = cv2.convexHull(contoursRed[i])
			cv2.drawContours(frame, [hull], -1, (0, 0, 255))
	for i in range(len(contoursGreen)):
		if cv2.contourArea(contoursGreen[i]) > 300:
			hull = cv2.convexHull(contoursGreen[i])
			cv2.drawContours(frame, [hull], -1, (0, 255, 0))

try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
	cv2.destroyAllWindows()