# Viết chương trình mỗi lần bấm BT1, động cơ servo quay một góc 5 độ
# khi quay đến 180 độ thì quay về 0, hiển thị GLCD
import RPi.GPIO as GPIO
import time


def main():
    BT1 = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global s
    s = sg90()  # khoi tao sg90
    # define cac goc quay khi bam cac nut
    anglepulseBT1 = 5
    print("All ready")
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("Move 5 angle")
            anglepulseBT1 = controlservo(s, anglepulseBT1)


def controlservo(s, anglepulseBT):
    # hàm này dùng để kiểm soát các góc quay của servo
    # Giá trị anglepulBT đưa vào sẽ làm quay servo quay theo góc đó
    # Khi góc quay >= 180 độ thì lần quay tiếp theo sẽ quay theo chiều
    # nguoc lai voi goc quay <= 0
    current = s.currentdirection()
    if current >= 180 or current <= 0:
        anglepulseBT = -anglepulseBT
    rotato = anglepulseBT + current  # vi tri se quay den
    rotato = 0 if (rotato >= 180 or rotato <= 0) else rotato
    s.setdirection(rotato, 40)  # quay den vi tri rotator
    time.sleep(0.5)
    # tra ve angleseBT moi de lan quay tiep theo
    # no se quay theo chieu am hoac duong
    return anglepulseBT


class sg90:
    # khoi tao servo voi tan so 50hz
    # No se nhan chu ki nhiem tu 2% den 12%
    # Gio no se chuyn no ve gia tri 0 den 180 cho de su dung
    def __init__(self):
        self.pin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)
        self.direction = 90

    def cleanup(self):
        # dung servo va giai phong GPIO
        self.servo.ChangDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection(self):
        # hien thi toc do hien tai cua servo
        return self.direction

    def _henkan(self, value):
        # chuyen cac gia tri 0 den 180 thanh 2 va 12
        return round(0.056 * value + 2.0)

    def setdirection(self, direction, speed):
        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction


try:
    main()
except KeyboardInterrupt:
    s.cleanup
