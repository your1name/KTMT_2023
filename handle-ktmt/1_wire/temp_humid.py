import time
import RPi.GPIO as GPIO 

def main():
    dht11 = 7
    instance = DHT11(pin=dht11)
    while True:
        temperature, humidity = instance.read()
        if temperature == 0 and humidity == 0 and humidity < 20:
            # gap loi thi se chay lai vong lap
            continue
        print("Temperature: %-3.1f C" % temperature)
        print("HUmidity: %-3.1f %%" % humidity)
        time.sleep(6)

class DHT11:
    def __init__(self, pin):
        self.pin = pin
        self.temparature = None
        self.humidity = None

    def read(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        # high
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.05)
        # low
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        # chuyen sang input va pull up 
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # thu thap du lieu 
        count = 0 
        last = -1 
        data = []
        while True:
            current = GPIO.input(self.pin)
            data.append(current)
            if last != current:
                count = 0
                last = current
            else:
                count += 1
                if count > 100:
                    break
        # phan tich do dai du lieu 
        pull_up_lengths = self.parse_data_pull_up_lengths(data)
        if len(pull_up_lengths) != 40:
            return (0,0)
        # tinh toan cac bit
        bits = self.calculate_bits(pull_up_lengths)
        # khi co bit, tinh toan cac byte
        the_bytes = self.bits_to_byte(bits)
        # y nghia cac gia tri cam bien tra ve
        # the_bytes[0]: humidity int 
        # the_bytes[1]: humidity decimal
        # the_bytes[2]: temperature int
        # the_bytes[3]: temperature decimal 
        self.temparature = the_bytes[2] + float(the_bytes[3])/10
        self.humidity = the_bytes[0] + float(the_bytes[1])/10
        return self.temparature, self.humidity 
        
    def parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        state = STATE_INIT_PULL_DOWN
        lengths = [] # chua do dai du lieu truoc
        current_length = 0 # chua do dai du lieu sau 
        for i in range(len(data)):
            current = data[i]
            current_length += 1
            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    state = STATE_DATA_FIRST_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue
        return lengths
    
    def calculate_bits(self, pull_up_lengths):
        # tim khoang thoi gian ngan nhat va dai nhat 
        shortest_pull_up = 1000
        longest_pull_up = 0
        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length
        # su dung halfway de xac dinh khoang thoi gian la dai hay ngan 
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up)/2
        bits = []
        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)
        return bits
    
    def bits_to_byte(self, bits):
        the_bytes = []
        byte = 0
        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i+1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0
        return the_bytes
    
try:
    main()
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()