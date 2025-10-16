# Play Fair Cipher Implementation in Python made by Samuel Kouřil
# GitHub: https://github.com/godblessamki/PlayFairCipher
# License: MIT License
# Date: 2023-10-05
table = [['' for _ in range(5)] for _ in range(5)]
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' is typically omitted in Playfair cipher
key = ""
def generate_table(key):
    global table
    key = key.upper().replace("J", "I")
    used = set()
    row, col = 0, 0

    for char in key:
        if char not in used and char in alphabet:
            used.add(char)
            table[row][col] = char
            col += 1
            if col == 5:
                col = 0
                row += 1

    for char in alphabet:
        if char not in used:
            used.add(char)
            table[row][col] = char
            col += 1
            if col == 5:
                col = 0
                row += 1
    return table
def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared = []
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i + 1]
            if char1 == char2:
                prepared.append(char1 + 'X')
                i += 1
            else:
                prepared.append(char1 + char2)
                i += 2
        else:
            prepared.append(char1 + 'X')
            i += 1
    return prepared
def find_position(char):
    for i in range(5):
        for j in range(5):
            if table[i][j] == char:
                return i, j
    return None
def encrypt(plaintext): 
    pairs = prepare_text(plaintext)
    ciphertext = ""
    for pair in pairs:
        row1, col1 = find_position(pair[0])
        row2, col2 = find_position(pair[1])
        if row1 == row2:
            ciphertext += table[row1][(col1 + 1) % 5]
            ciphertext += table[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += table[(row1 + 1) % 5][col1]
            ciphertext += table[(row2 + 1) % 5][col2]
        else:
            ciphertext += table[row1][col2]
            ciphertext += table[row2][col1]
    return ciphertext
def decrypt(ciphertext):
    pairs = prepare_text(ciphertext)
    plaintext = ""
    for pair in pairs:
        row1, col1 = find_position(pair[0])
        row2, col2 = find_position(pair[1])
        if row1 == row2:
            plaintext += table[row1][(col1 - 1) % 5]
            plaintext += table[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += table[(row1 - 1) % 5][col1]
            plaintext += table[(row2 - 1) % 5][col2]
        else:
            plaintext += table[row1][col2]
            plaintext += table[row2][col1]
    return plaintext
if __name__ == "__main__":
    key = input("Enter the key: ")
    generate_table(key)
    print("Generated Table:")
    for row in table:
        print(' '.join(row))
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").upper()
    if choice == 'E':
        plaintext = input("Enter plaintext: ")
        ciphertext = encrypt(plaintext)
        print(f"Ciphertext: {ciphertext}")
    elif choice == 'D':
        ciphertext = input("Enter ciphertext: ")
        plaintext = decrypt(ciphertext)
        print(f"Plaintext: {plaintext}")
    else:
        print("Invalid choice. Please enter 'E' or 'D'.")
        