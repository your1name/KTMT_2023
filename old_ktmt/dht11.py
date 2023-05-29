# Viết chương trình đọc giá trị nhiệt độ, độ ẩm của cảm biến DHT11
# hiển thị giá trị lên terminal
import time
import RPi.GPIO as GPIO


def main():
    dht11 = 24
    instance = DHT11(pin=dht11)
    while True:
        temperature, humidity = instance.read()
        if temperature == 0 and humidity == 0 and humidity < 20:
            continue
        print("Temperature: %-3.1f C" % temperature)
        print("Humidity: %-3.1f %%" % humidity)
        print("---------------------------------------------")
        time.sleep(6)


class DHT11:
    def __init__(self, pin):
        self.pin = pin
        self.temperature = None
        self.humidity = None

    def read(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        pull_up_lengths = self.parse_data_pull_up_lengths(data)
        if len(pull_up_lengths) != 40:
            return (0, 0)
        bits = self.calculate_bits(pull_up_lengths)
        the_bytes = self.bits_to_bytes(bits)
        self.temperature = the_bytes[2] + float(the_bytes[3]) / 10
        self.humidity = the_bytes[0] + float(the_bytes[1]) / 10
        return self.temperature, self.humidity

    def parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        state = STATE_INIT_PULL_DOWN
        lengths = []
        current_length = 0
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
        shortest_pull_up = 1000
        longest_pull_up = 0
        for i in range(len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length
            halfway = shortest_pull_up + \
                (longest_pull_up - shortest_pull_up) / 2
            bits = []
            for i in range(len(pull_up_lengths)):
                bit = False
                if pull_up_lengths[i] > halfway:
                    bit = True
                bits.append(bit)
            return bits

    def bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0
        for i in range(0, len(bits)):
            byte = byte << 1
            if bits[i]:
                byte = byte | 1
            else:
                byte = byte | 0
            if (i+1) % 8 == 0:
                the_bytes.append(byte)
                byte = 0
        return the_bytes


try:
    main()
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
