import re

with open(r'PATH TO YOUR TXT FILE', 'r', encoding='utf-8') as file:
    potter = file.read()

potter = potter.lower()
potter = re.sub(r'[^a-z]', '', potter)

letter_counts = {
    'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0,
    'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0,
    'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0,
    'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0,
    'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
}

flag = 0
words = 40000
heck=0

for char in potter:
    if char in letter_counts:
        letter_counts[char] += 1
    
    flag += 1

    if flag == words:
        print("end")
        break

for letter, count in letter_counts.items():

    num = 0
    num =  round((count / words) * 100, 2)

    print(f"Litera '{letter}'to {num}")
    heck +=num

print(heck)