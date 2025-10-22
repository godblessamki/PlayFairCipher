# PlayFair Cipher

A Python implementation of the Playfair cipher, a manual symmetric encryption technique invented by Charles Wheatstone in 1854.

## What is the Playfair Cipher?

The Playfair cipher is a digraph substitution cipher that encrypts pairs of letters instead of single letters. It uses a 5x5 matrix of letters constructed using a keyword, making it more secure than simple substitution ciphers.

## Features

- Encrypt text using the Playfair cipher algorithm
- Decrypt Playfair-encrypted messages
- Generate 5x5 key matrices from custom keywords
- Handle special cases (duplicate letters, odd-length messages)

## Installation

Clone this repository:

```bash
git clone https://github.com/godblessamki/PlayFairCipher.git
cd PlayFairCipher
```

## Usage

```python
# Example usage (adjust based on your actual implementation)
from playfair import PlayfairCipher

# Create cipher with a keyword
cipher = PlayfairCipher("KEYWORD")

# Encrypt a message
encrypted = cipher.encrypt("HELLO WORLD")
print(f"Encrypted: {encrypted}")

# Decrypt a message
decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")
```

## How It Works

1. **Key Matrix Generation**: A 5x5 matrix is created using a keyword, with I/J sharing the same position
2. **Text Preparation**: The plaintext is prepared by removing spaces and splitting into digraphs (pairs)
3. **Encryption Rules**:
   - If both letters are in the same row, shift right
   - If both letters are in the same column, shift down
   - If in different rows/columns, form a rectangle and swap corners

## Requirements

- Python 3.x

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

[@godblessamki](https://github.com/godblessamki)

## Acknowledgments

- Based on the Playfair cipher algorithm developed by Charles Wheatstone
- Named after Lord Playfair who promoted its use
```
