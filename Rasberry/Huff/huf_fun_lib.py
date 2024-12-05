"""This script is used to contain functions for Huffman coding"""

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

# text = huf_input()
# print(text)
# print(huf_output(text))
