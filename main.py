# Play Fair Cipher Implementation in Python
# Made by Samuel Kouřil (updated)
# License: MIT License

class PlayfairCipher:
    def __init__(self):
        self.table = [['' for _ in range(5)] for _ in range(5)]
        
        # Diakritická mapa pro české znaky
        self.DIACRITIC_MAP = {
            'Á': 'A', 'á': 'A', 'Č': 'C', 'č': 'C', 'Ď': 'D', 'ď': 'D',
            'É': 'E', 'é': 'E', 'Ě': 'E', 'ě': 'E', 'Í': 'I', 'í': 'I',
            'Ň': 'N', 'ň': 'N', 'Ó': 'O', 'ó': 'O', 'Ř': 'R', 'ř': 'R',
            'Š': 'S', 'š': 'S', 'Ť': 'T', 'ť': 'T', 'Ú': 'U', 'ú': 'U',
            'Ů': 'U', 'ů': 'U', 'Ý': 'Y', 'ý': 'Y', 'Ž': 'Z', 'ž': 'Z',
        }

        # Abecedy
        self.ALPHABET_EN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # bez J
        self.ALPHABET_CZ = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # bez W

        # Aktuální nastavení
        self.current_alphabet = self.ALPHABET_EN
        self.replace_char = 'J'
        self.padding_char = 'X'
        self.secondary_padding_char = 'Q'

        # Globální úložiště pro metadata
        self.last_encryption_metadata = None

    def set_language(self, lang='EN'):
        """Nastaví jazyk šifry (EN nebo CZ)"""
        if lang.upper() == 'CZ':
            self.current_alphabet = self.ALPHABET_CZ
            self.replace_char = 'W'
        else:
            self.current_alphabet = self.ALPHABET_EN
            self.replace_char = 'J'

    def filter_text(self, text):
        """Filtruje vstupní text - odstraní speciální znaky, převede diakritiku."""
        filtered = []
        spaces_positions = []
        special_data = []
        
        filtered_index = 0
        for original_index, char in enumerate(text):
            if char == ' ':
                spaces_positions.append(original_index)
                continue
            
            if not char.isalpha():
                special_data.append((original_index, char))
                continue
            
            if char in self.DIACRITIC_MAP:
                char = self.DIACRITIC_MAP[char]
            
            char = char.upper()
            
            if char == self.replace_char:
                char = 'I' if self.replace_char == 'J' else 'V'
            
            if char in self.current_alphabet:
                filtered.append(char)
                filtered_index += 1
        
        return ''.join(filtered), spaces_positions, special_data

    def restore_spaces_and_special(self, decrypted_text, spaces_positions, special_data, padding_positions):
        """Obnoví mezery a speciální znaky na původní pozice."""
        decrypted_chars = list(decrypted_text.upper())
        
        for pos in sorted(padding_positions, reverse=True):
            if pos < len(decrypted_chars):
                del decrypted_chars[pos]
        
        decrypted_chars = [char.lower() for char in decrypted_chars]
        
        result = []
        decrypted_index = 0
        original_length = len(decrypted_chars) + len(spaces_positions) + len(special_data)
        
        for i in range(original_length):
            special_found = False
            for spec_pos, spec_char in special_data:
                if spec_pos == i:
                    result.append(spec_char)
                    special_found = True
                    break
            
            if special_found:
                continue
                
            if i in spaces_positions:
                result.append(' ')
            else:
                if decrypted_index < len(decrypted_chars):
                    result.append(decrypted_chars[decrypted_index])
                    decrypted_index += 1
        
        return ''.join(result)

    def generate_table(self, key):
        """Generuje šifrovací tabulku 5x5 z klíče"""
        key_filtered, _, _ = self.filter_text(key)
        
        used = set()
        row, col = 0, 0
        
        for char in key_filtered:
            if char not in used and char in self.current_alphabet:
                used.add(char)
                self.table[row][col] = char
                col += 1
                if col == 5:
                    col = 0
                    row += 1
        
        for char in self.current_alphabet:
            if char not in used:
                used.add(char)
                self.table[row][col] = char
                col += 1
                if col == 5:
                    col = 0
                    row += 1
        
        return self.table

    def prepare_text(self, text):
        """Připraví text pro šifrování - vytvoří bigramy."""
        prepared = []
        padding_positions = []
        i = 0
        
        while i < len(text):
            if i + 1 >= len(text):
                char1 = text[i]
                padding = self.padding_char if char1 != self.padding_char else self.secondary_padding_char
                prepared.append(char1 + padding)
                padding_positions.append(i + 1)
                break
            
            char1 = text[i]
            char2 = text[i + 1]
            
            if char1 == char2:
                padding = self.padding_char if char1 != self.padding_char else self.secondary_padding_char
                prepared.append(char1 + padding)
                padding_positions.append(i + 1)
                i += 1
            else:
                prepared.append(char1 + char2)
                i += 2
        
        return prepared, padding_positions

    def find_position(self, char):
        """Najde pozici znaku v tabulce"""
        for i in range(5):
            for j in range(5):
                if self.table[i][j] == char:
                    return i, j
        return None

    def encrypt(self, plaintext):
        """Šifruje otevřený text pomocí Playfair šifry."""
        filtered_text, spaces_pos, special_data = self.filter_text(plaintext)
        
        pairs, padding_positions = self.prepare_text(filtered_text)
        
        self.last_encryption_metadata = {
            'spaces': spaces_pos,
            'special': special_data,
            'padding_positions': padding_positions
        }
        
        ciphertext = ""
        
        for pair in pairs:
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])
            
            if row1 is None or row2 is None:
                continue
                
            if row1 == row2:
                ciphertext += self.table[row1][(col1 + 1) % 5]
                ciphertext += self.table[row2][(col2 + 1) % 5]
            elif col1 == col2:
                ciphertext += self.table[(row1 + 1) % 5][col1]
                ciphertext += self.table[(row2 + 1) % 5][col2]
            else:
                ciphertext += self.table[row1][col2]
                ciphertext += self.table[row2][col1]
        
        formatted = ' '.join([ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)])
        
        return formatted, pairs, filtered_text, spaces_pos, special_data

    def decrypt(self, ciphertext, spaces_pos=None, special_data=None, padding_positions=None):
        """Dešifruje šifrovaný text pomocí Playfair šifry."""
        if spaces_pos is None and special_data is None and self.last_encryption_metadata:
            spaces_pos = self.last_encryption_metadata['spaces']
            special_data = self.last_encryption_metadata['special']
            padding_positions = self.last_encryption_metadata['padding_positions']
        
        filtered_cipher, _, _ = self.filter_text(ciphertext)
        
        pairs = [filtered_cipher[i:i+2] for i in range(0, len(filtered_cipher), 2)]
        
        plaintext = ""
        
        for pair in pairs:
            if len(pair) != 2:
                continue
                
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])
            
            if row1 is None or row2 is None:
                continue
                
            if row1 == row2:
                plaintext += self.table[row1][(col1 - 1) % 5]
                plaintext += self.table[row2][(col2 - 1) % 5]
            elif col1 == col2:
                plaintext += self.table[(row1 - 1) % 5][col1]
                plaintext += self.table[(row2 - 1) % 5][col2]
            else:
                plaintext += self.table[row1][col2]
                plaintext += self.table[row2][col1]
        
        if spaces_pos is not None and special_data is not None and padding_positions is not None:
            plaintext = self.restore_spaces_and_special(plaintext, spaces_pos, special_data, padding_positions)
        
        return plaintext

    def get_table(self):
        """Vrátí aktuální šifrovací tabulku"""
        return self.table

# Spuštění GUI
if __name__ == "__main__":
    from playfair_gui import PlayfairGUI
    import tkinter as tk
    
    cipher = PlayfairCipher()
    root = tk.Tk()
    app = PlayfairGUI(root, cipher)
    root.mainloop()