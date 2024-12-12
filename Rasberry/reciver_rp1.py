import RPi.GPIO as GPIO
import time
import threading
import json
import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.platform.asyncio
import asyncio

# Constants
clock_freq = 0.06
safety_clock_freq = 0.0005
reciving_pin = 14
sending_pin = 15

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)

# List of connected clients
connected_clients = set()


class MyWebSocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("Client connected")
        connected_clients.add(self)

    def on_message(self, message):
        # print("Received message:", message)
        data = json.loads(message)
        msg_type = data.get("type")
        user = data.get("user")
        msg_data = data.get("data")

        if msg_type == "message":
            # Determine sender and broadcast the message
            print(msg_data)
            huf_input(msg_data)
            # self.write_message(json.dumps({ "type": "message", "user": "Server", "data": msg_data}))

        elif msg_type == "typing":
            # Broadcast typing indicator
            print("typing")
        # Uncomment to send a response back to the client
        # self.write_message(json.dumps({ "type": "message", "user": "Server", "data": "Hello from server"}))
    
    def send_mess(self):
        self.write_message(json.dumps({ "type": "message", "user": "Other client", "data": "Hello from server"}))

    def on_close(self):
        print("Client disconnected")
        connected_clients.discard(self)

# Start the WebSocket server
async def start_tornado_server():
    """Start the Tornado WebSocket server."""
    print("Starting Tornado WebSocket server...")
    
    # Integrate Tornado with asyncio
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    # Create the Tornado application
    app = tornado.web.Application([
        (r"/websocket", MyWebSocketHandler),
    ])
    app.listen(8888)
    print("WebSocket server started on ws://localhost:8888/websocket")

    # Keep the server running
    await asyncio.Future()  # Equivalent to running forever

def broadcast_message(message):
    for client in connected_clients:
        if not client.ws_connection or not client.ws_connection.stream.socket:
            # Skip closed connections
            continue
        try:
            client.write_message(message)
        except Exception as e:
            print(f"Error sending message to client: {e}")

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
    

def huf_input(inpt):
    # inpt = input()
    print("huf input")
    converted_input = ''.join(convert_char_to_number(char) for char in inpt)
    encoded = huffman_encode(converted_input, huffman_code)
    send_data(encoded)

def huf_output(output):
    decoded_output = huffman_decode(output, huffman_code)
    converted_output = conv_string(decoded_output)
    # WebSocketHandler.write_message(converted_output)
    broadcast_message(json.dumps({ "type": "message", "user": "Other client", "data": converted_output}))
    return converted_output

def send_data(input_user):
    # input_user= huf_input()
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.LOW)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq*3)
    GPIO.output(sending_pin, GPIO.LOW)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq*3)
    for i in input_user:
        if i == '0':
            GPIO.output(sending_pin, GPIO.LOW)
            time.sleep(clock_freq)
        else:
            GPIO.output(sending_pin, GPIO.HIGH)
            time.sleep(clock_freq)
    print("stop")
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.LOW)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq*3)
    GPIO.output(sending_pin, GPIO.LOW)
    time.sleep(clock_freq)
    GPIO.output(sending_pin, GPIO.HIGH)
    time.sleep(clock_freq*3)
    GPIO.output(sending_pin, GPIO.LOW)


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
                                                            #print("recived..",recived )
                                                            time.sleep(clock_freq)     
                                                        else:
                                                            recived = recived + "0"
                                                            # print("recived..", recived)
                                                            time.sleep(clock_freq)
                                                        if recived.endswith("1011110111") and len(recived) > 10:
                                                            flag = True
                                                            break
        if flag == True:
            recived = recived[0:-10]
            print(huf_output(recived)) # tu wyciagac po tej sie resetuje
            recived = ""
            flag = False
            GPIO.event_detected(reciving_pin)


try:
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
                            break

                            
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
    time.sleep(0.1)
    if GPIO.event_detected(reciving_pin): #event detection has to stay
        print("reciving...")

    listener_thread = threading.Thread(target=listen_for_data, daemon=True)
    listener_thread.start()

    asyncio.run(start_tornado_server())

    # sender_thread = threading.Thread(target=send_data, daemon=True)
    # sender_thread.start()

    # websocket_thread = threading.Thread(target=asyncio.run(start_tornado_server()), daemon=True)
    # websocket_thread.start()

    
    '''sender message code  1011110111  - 99 (if in code numbers above and including 80 appear the system won't work)'''
    '''reciver message code 101110111   - 98'''

    

except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()

# opcjonalnie spacja na stronie wysyła do pythona i przesyła 