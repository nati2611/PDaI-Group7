import os
from collections import Counter

def count_digits_in_file(file_path):
    """Zlicza wystąpienia każdej cyfry w pliku."""
    with open(file_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    digits = [char for char in content if char.isdigit()]
    return Counter(digits)

def count_digits_in_folder(input_folder):
    """Zlicza wystąpienia cyfr we wszystkich plikach w folderze."""
    total_counts = Counter()
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_folder, filename)
            file_counts = count_digits_in_file(file_path)
            total_counts.update(file_counts)
            print(f"Przetworzono: {filename}")
    
    return total_counts

def calculate_ratios(counts):
    """Oblicza stosunek wystąpień każdej cyfry do sumy wszystkich wystąpień."""
    total = sum(counts.values())
    ratios = {key: value / total for key, value in counts.items()}
    return ratios


input_folder = 'HP_num'

counts = count_digits_in_folder(input_folder)

ratios = calculate_ratios(counts)

print("\nCount:")
for digit in sorted(counts):  
    print(f"Digit {digit}: {counts[digit]}")

sum = 0
print("\nPercentage:")
for digit in sorted(ratios): 
    print(f"Digit {digit}: {ratios[digit]}")
    sum += ratios[digit]

print(f"Sum: {sum}" )