import os

""" This script is used to prepare files to calculate statistic according to Huffman coding"""

char_to_number = {
    **{chr(i): i - 96 for i in range(97, 123)},  # a-z (1-26)
    **{chr(i): i - 38 for i in range(65, 91)},  # A-Z (27-52)
    **{str(i): 53 + i for i in range(10)},      # 0-9 (53-62)
    ' ': 63, '.': 64, ',': 65, "'": 66, '': 67, '-': 68, '!': 69, '?': 70, '(': 71, ')': 72, ':': 73, ';': 74
}

def convert_char_to_number(char):
    """Converts char into two number digit long according to key."""
    number = char_to_number.get(char, 0)
    return f"{number:02d}"

def process_file(input_path, output_path):
    """Works on txt file, sends chars to  zapisując wynik."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    converted_content = ' '.join(convert_char_to_number(char) for char in content)
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_content)

def process_folder(input_folder, output_folder):
    """Przetwarza wszystkie pliki .txt w folderze."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"converted_{filename}")
            process_file(input_path, output_path)
            print(f"Przetworzono: {filename} -> {output_path}")

input_folder = 'HP'
output_folder = 'HP_num'

process_folder(input_folder, output_folder)
