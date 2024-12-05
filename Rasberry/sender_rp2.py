import RPi.GPIO as GPIO
import time
import threading
# import huf_fun_lib

clock_freq = 0.06
safety_clock_freq= 0.0005
reciving_pin = 14
sending_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)

def huffman_encode(data, huffman_code):
    if not data:
        return ""
    
    try:
        encoded_data = ''.join(huffman_code[char] for char in data)
    except KeyError as e:
        raise ValueError(f"Char '{e.args[0]}' not implemented Huffman.")
    
    return encoded_data


def huffman_decode(encoded_data, huffman_code):
    if not encoded_data or not huffman_code:
        return ""
    
    reverse_code = {code: char for char, code in huffman_code.items()}
    decoded_data = ""
    buffer = ""
    
    for bit in encoded_data:
        buffer += bit
        if buffer in reverse_code:
            decoded_data += reverse_code[buffer]
            buffer = ""
    
    return decoded_data


huffman_code = {
    '0': '00',
    '1': '100',
    '2': '1010',
    '3': '110',
    '4': '0110',
    '5': '010',
    '6': '111',
    '7': '10110',
    '8': '0111',
    '9': '10111'
}

char_to_number = {
    **{chr(i): i - 96 for i in range(97, 123)},  # a-z (1-26)
    **{chr(i): i - 38 for i in range(65, 91)},  # A-Z (27-52)
    **{str(i): 53 + i for i in range(10)},      # 0-9 (53-62)
    ' ': 63, '.': 64, ',': 65, "'": 66, '': 67, '-': 68, '!': 69, '?': 70, '(': 71, ')': 72, ':': 73, ';': 74
}

def convert_char_to_number(char):
    """Converting char to two digit number accordin to key."""
    number = char_to_number.get(char, 0)
    return f"{number:02d}"

number_to_char = {v: k for k, v in char_to_number.items()}

def convert_number_to_char(number):
    """Converting two digit number to char accordin to key."""
    try:
        num = int(number)
        return number_to_char.get(num, '?')
    except ValueError:
        return '?'
    
def conv_string(encoded_string):
    """Converts whole string to two digits and sends to convert_number_to_char function to convert into char."""
    decoded_chars = []
    for i in range(0, len(encoded_string), 2):
        number = encoded_string[i:i+2]
        decoded_chars.append(convert_number_to_char(number))
    return ''.join(decoded_chars)
    

def huf_input():
    inpt = input()
    converted_input = ''.join(convert_char_to_number(char) for char in inpt)
    encoded = huffman_encode(converted_input, huffman_code)
    return encoded

def huf_output(output):
    decoded_output = huffman_decode(output, huffman_code)
    converted_output = conv_string(decoded_output)
    return converted_output

def listen_for_data():
    recived= ""
    flag = False
    while True:
        time.sleep(safety_clock_freq)
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                time.sleep(clock_freq)  
                if GPIO.input(reciving_pin) == GPIO.LOW:
                    time.sleep(clock_freq)
                    if GPIO.input(reciving_pin) == GPIO.HIGH:
                        time.sleep(clock_freq)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            time.sleep(clock_freq)
                            if GPIO.input(reciving_pin) == GPIO.HIGH:
                                time.sleep(clock_freq)
                                if GPIO.input(reciving_pin) == GPIO.LOW:
                                    time.sleep(clock_freq)
                                    if GPIO.input(reciving_pin) == GPIO.HIGH:
                                        time.sleep(clock_freq)
                                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                                            time.sleep(clock_freq)
                                            if GPIO.input(reciving_pin) == GPIO.HIGH:
                                                time.sleep(clock_freq)
                                                while True:
                                                    if GPIO.input(reciving_pin) == GPIO.HIGH:
                                                        recived = recived + "1"
                                                        # print("recived..",recived )
                                                        time.sleep(clock_freq)     
                                                    else:
                                                        recived = recived + "0"
                                                        # print("recived..", recived)
                                                        time.sleep(clock_freq)
                                                    if recived.endswith("101110111") and len(recived) > 9:
                                                        flag = True
                                                        break
        if flag == True:
                recived = recived[0:-9]
                print(huf_output(recived))
                recived = ""
                flag = False
                GPIO.event_detected(reciving_pin)



try:
    time.sleep(clock_freq)
    while True:
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq)
        break
    GPIO.output(sending_pin, GPIO.LOW)
    while True:
        time.sleep(safety_clock_freq)
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                time.sleep(clock_freq)  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    time.sleep(clock_freq)
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        time.sleep(clock_freq)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("connect")
                            time.sleep(clock_freq)
                            listener_thread = threading.Thread(target=listen_for_data, daemon=True)
                            listener_thread.start()
                            break
    
    

    '''sender message code  1011110111  - 99 (if in code numbers above and including 80 appear the system won't work)'''
    '''reciver message code 101110111   - 98'''

    while True:
        input_user= huf_input() # i tu 
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq*4)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq*3)
        for i in input_user:
            if i == '0':
                GPIO.output(sending_pin, GPIO.LOW)
                time.sleep(clock_freq)
            if i == '1':
                GPIO.output(sending_pin, GPIO.HIGH)
                time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq*4)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(clock_freq*3)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(clock_freq)
        print("stop")

except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()
