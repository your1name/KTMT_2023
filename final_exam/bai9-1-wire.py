# Đo nhiệt, ẩm, hiển thị LCD
import time
import RPi.GPIO as GPIO


# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
# Define some divice constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # 1 LCD RAM add
LCD_LINE_2 = 0xC0 # 2 LCD RAM add
#Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def lcd_init():
    GPIO.setmode(GPIO.BCM) # uses BCM GPIO numbers
    GPIO.setwarnings(False) 
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5        
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # backlight enabls
    #Initalise display
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)

def lcd_string(message, position, line):
    message = message.rjust(len(message) + position)
    if line == 1:
        lcd_byte(LCD_LINE_1, False)
    else:
        lcd_byte(LCD_LINE_2, False)
    for i in range(len(message)):
        lcd_byte(ord(message[i]), LCD_CHR)

def lcd_clear():
    lcd_string("             ", 0,1)
    lcd_string("             ",0, 2)

# Very headache function
def lcd_byte(bits, mode):
    # Send byte to data point
    # bits = data
    # mode = True for character
    #        False for conmand
    GPIO.output(LCD_RS, mode) # RS
    # High bits
    GPIO.output(LCD_D4, False) 
    GPIO.output(LCD_D5, False) 
    GPIO.output(LCD_D6, False) 
    GPIO.output(LCD_D7, False)


    if bits&0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80 == 0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    # low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def main():
    lcd_init()
    time.sleep(1)
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)

    dht11 = 7
    instance = DHT11(pin = dht11)
    while True:
        temperature, humidity = instance.read()
        if temperature == 0 and humidity == 0 and humidity < 20:
            # xu li khi gap loi, no se chay lai vong lap
            continue

        # text = str(round(temperature,1))+ 'C, ' + str(round(humidity,1)) + '%'
        # lcd_string(text, 0, 1)

        nhiet = 'nhiet: ' + str(round(temperature,1))+ 'C'
        am = 'am: ' +  str(round(humidity,1)) + '%'
        lcd_string(nhiet, 0, 1)
        lcd_string(am, 0, 2)
        
        print('temperature: %-3.1f C' % temperature)
        print('humidity: %-3.1f %%' % humidity)
        time.sleep(6)


class DHT11:
    def __init__(self, pin):
        self.pin = pin
        self.temperature = None
        self.humidity = None
    
    def read(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        # HIGH
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.05)
        # LOW
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        # chuyen sang input vaf pull_up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
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
    
        # phan tich do dai cua du lieu
        pull_up_lengths = self.parse_data_pull_up_lengths(data)
        if len(pull_up_lengths) != 40:
            return (0, 0)
        # tinh toan cac bit 
        bits = self.calculate_bits(pull_up_lengths)
        # khi co bit, tinh toan cac byte

        the_bytes = self.bits_to_bytes(bits)
        # y nghia cac gia tri cam bien tra ve
        # the_bytes[0] = humidity int 
        # the_bytes[1] = humidity decimal
        # the_bytes[2] = temperature int
        # the_bytes[3] = temperature decimal
       
        self.temperature = the_bytes[2] + float(the_bytes[3])/10
        self.humidity = the_bytes[0] + float(the_bytes[1])/10
        return self.temperature, self.humidity 
    
    def parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        
        state = STATE_INIT_PULL_DOWN
        lengths = [] # Nó sẽ chứa độ dài dữ liệu trước
        current_length = 0 # nó sẽ chứa độ dài dữ liệu sau
        for i in range(len(data)):
            current = data[i]
            current_length += 1
            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    # ok, ta đã khởi tạo nó vs pull down
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                    continue

            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    # ok, ta đã khởi tạo nó vs pull up
                    state = STATE_DATA_FIRST_PULL_DOWN
                    continue
                else:
                    continue 

            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    # ok, ta đã khởi tạo nó vs pull down
                    # tiếp theo sẽ là dữ liệu pull up
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue

            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    # data pulled up, độ dài pull up quyết định đâu là 0 hoặc 1
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                    continue
                else:
                    continue
            
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    # pulled down, ta lưu trữ độ dài của pull up trước
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue
        return lengths
    def calculate_bits(self, pull_up_lengths):
        # tim khoang thời gian ngắn nhất và dài nhất
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length
        # su dung halfway để xác định xem khoảng time đố là dài hay ngắn
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up)/2
        bits = []
        for i in range(0, len(pull_up_lengths)):
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
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0

            if ((i +1) % 8 ==0) :
                the_bytes.append(byte)
                byte = 0
        return the_bytes

try:
    main()
except KeyboardInterrupt:
    print('cleanup')
    GPIO.cleanup()
            
                