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

data = "1234567890"

encoded = huffman_encode(data, huffman_code)
print("Zakodowane dane:", encoded)

decoded = huffman_decode(encoded, huffman_code)
print("Odkodowane dane:", decoded)
