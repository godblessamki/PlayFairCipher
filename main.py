# Play Fair Cipher Implementation in Python
# Made by Samuel Kouřil (updated)
# License: MIT License

class PlayfairCipher:
    def __init__(self):
        # Inicializace matice 5x5 pro šifrovací tabulku
        self.table = [['' for _ in range(5)] for _ in range(5)]
        
        # Diakritická mapa pro české znaky (odstranění diakritiky)
        self.DIACRITIC_MAP = {
            'Á': 'A', 'á': 'A', 'Č': 'C', 'č': 'C', 'Ď': 'D', 'ď': 'D',
            'É': 'E', 'é': 'E', 'Ě': 'E', 'ě': 'E', 'Í': 'I', 'í': 'I',
            'Ň': 'N', 'ň': 'N', 'Ó': 'O', 'ó': 'O', 'Ř': 'R', 'ř': 'R',
            'Š': 'S', 'š': 'S', 'Ť': 'T', 'ť': 'T', 'Ú': 'U', 'ú': 'U',
            'Ů': 'U', 'ů': 'U', 'Ý': 'Y', 'ý': 'Y', 'Ž': 'Z', 'ž': 'Z',
        }

        # Abecedy (25 znaků)
        self.ALPHABET_EN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # bez J
        self.ALPHABET_CZ = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # bez W

        # Aktuální nastavení
        self.current_alphabet = self.ALPHABET_EN
        self.replace_char = 'J'             # Znak, který se nahrazuje (J -> I, W -> V)
        self.padding_char = 'X'             # Primární výplňový znak do bigramů
        self.secondary_padding_char = 'Q'   # Sekundární výplňový znak
        
        # Globální úložiště pro metadata (pouze mezery a výplně)
        self.last_encryption_metadata = None

    def set_language(self, lang='EN'):
        """Nastaví jazyk šifry (EN nebo CZ) a s ním související nahrazovaný znak."""
        if lang.upper() == 'CZ':
            self.current_alphabet = self.ALPHABET_CZ
            self.replace_char = 'W'
        else:
            self.current_alphabet = self.ALPHABET_EN
            self.replace_char = 'J'

    def filter_text(self, text):
        """
        Filtruje vstupní text: odstraní diakritiku, převede na velká písmena.
        Mezery se ukládají pro obnovu, SPECIÁLNÍ ZNAKY JSOU KOMPLETNĚ VYMAZÁNY.
        """
        filtered = []
        spaces_positions = []
        
        for original_index, char in enumerate(text):
            # 1. Zpracování mezer (ty se stále ukládají pro obnovu)
            if char == ' ':
                spaces_positions.append(original_index)
                continue
            
            # 2. Vypuštění speciálních znaků
            if not char.isalpha(): 
                continue # Pokud není písmeno, ignorujeme ho (vymažeme)
            
            # 3. Odstranění diakritiky
            if char in self.DIACRITIC_MAP:
                char = self.DIACRITIC_MAP[char]
            
            # 4. Normalizace a substituce J/W
            char = char.upper()
            
            if char == self.replace_char:
                # J se nahrazuje I (EN), W se nahrazuje V (CZ)
                char = 'I' if self.replace_char == 'J' else 'V'
            
            # 5. Zápis platných znaků
            if char in self.current_alphabet:
                filtered.append(char)
        
        # Vrací jen metadata pro mezery
        return ''.join(filtered), spaces_positions

    def restore_spaces_and_special(self, decrypted_text, spaces_positions, padding_positions):
        """
        Obnoví mezery na původní pozice a odstraní výplňové znaky.
        Speciální znaky se NEobnovují.
        """
        decrypted_chars = list(decrypted_text.upper())
        
        # Odstranění výplňových znaků (od konce)
        for pos in sorted(padding_positions, reverse=True):
            if pos < len(decrypted_chars):
                del decrypted_chars[pos]
        
        # Převedení výsledku na malá písmena
        decrypted_chars = [char.lower() for char in decrypted_chars]
        
        result = []
        decrypted_index = 0
        
        # Výpočet původní délky (pouze znaky + mezery)
        original_length = len(decrypted_chars) + len(spaces_positions)
        
        for i in range(original_length):
            if i in spaces_positions:
                result.append(' ') # Vloží mezeru
            else:
                # Vloží dešifrovaný znak
                if decrypted_index < len(decrypted_chars):
                    result.append(decrypted_chars[decrypted_index])
                    decrypted_index += 1
        
        return ''.join(result)

    def generate_table(self, key):
        """
        Generuje šifrovací tabulku 5x5 z klíče.
        
        """
        # filter_text se volá pro klíč, speciální znaky jsou ignorovány
        key_filtered, _ = self.filter_text(key) 
        
        used = set()
        row, col = 0, 0
        
        # 1. Fáze: Znaky z klíče
        for char in key_filtered:
            if char not in used and char in self.current_alphabet:
                used.add(char)
                self.table[row][col] = char
                col += 1
                if col == 5:
                    col = 0
                    row += 1
        
        # 2. Fáze: Zbytek abecedy
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
        """Připraví text pro šifrování: rozdělení na bigramy a vložení výplní."""
        prepared = []
        padding_positions = []
        i = 0
        
        while i < len(text):
            # Pravidlo 1: Lichý počet znaků (doplnění na konec)
            if i + 1 >= len(text):
                char1 = text[i]
                padding = self.padding_char if char1 != self.padding_char else self.secondary_padding_char
                prepared.append(char1 + padding)
                padding_positions.append(i + 1)
                break
            
            char1 = text[i]
            char2 = text[i + 1]
            
            # Pravidlo 2: Stejné znaky v páru (vložení výplně)
            if char1 == char2:
                padding = self.padding_char if char1 != self.padding_char else self.secondary_padding_char
                prepared.append(char1 + padding)
                padding_positions.append(i + 1)
                i += 1 # Posun jen o 1, aby se druhý shodný znak zpracoval v dalším kroku
            else:
                # Pravidlo 3: Běžný pár
                prepared.append(char1 + char2)
                i += 2
        
        return prepared, padding_positions

    def find_position(self, char):
        """Najde pozici znaku v tabulce (řádek, sloupec)"""
        for i in range(5):
            for j in range(5):
                if self.table[i][j] == char:
                    return i, j
        return None

    def encrypt(self, plaintext):
        """Šifruje otevřený text pomocí Playfair šifry."""
        # filter_text nyní vrací jen filtered_text a spaces_pos
        filtered_text, spaces_pos = self.filter_text(plaintext)
        
        pairs, padding_positions = self.prepare_text(filtered_text)
        
        # Uložíme pouze pozice mezer a výplní
        self.last_encryption_metadata = {
            'spaces': spaces_pos,
            'padding_positions': padding_positions
        }
        
        ciphertext = ""
        
        for pair in pairs:
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])
            
            if row1 is None or row2 is None:
                continue
                
            # Pravidlo 1: Stejný řádek (posun doprava)
            if row1 == row2:
                ciphertext += self.table[row1][(col1 + 1) % 5]
                ciphertext += self.table[row2][(col2 + 1) % 5]
            # Pravidlo 2: Stejný sloupec (posun dolů)
            elif col1 == col2:
                ciphertext += self.table[(row1 + 1) % 5][col1]
                ciphertext += self.table[(row2 + 1) % 5][col2]
            # Pravidlo 3: Obdélník (záměna sloupců)
            else:
                ciphertext += self.table[row1][col2]
                ciphertext += self.table[row2][col1]
        
        # Formátování výstupu do skupin po 5
        formatted = ' '.join([ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)])
        
        # Vracíme bez special_data
        return formatted, pairs, filtered_text, spaces_pos

    def decrypt(self, ciphertext, spaces_pos=None, padding_positions=None):
        """Dešifruje šifrovaný text pomocí Playfair šifry."""
        
        # Načtení metadat pro obnovu (pokud nejsou předána)
        if spaces_pos is None and self.last_encryption_metadata:
            spaces_pos = self.last_encryption_metadata.get('spaces')
            padding_positions = self.last_encryption_metadata.get('padding_positions')
        
        # Filtr textu (odstranění formátovacích mezer)
        filtered_cipher, _ = self.filter_text(ciphertext)
        
        pairs = [filtered_cipher[i:i+2] for i in range(0, len(filtered_cipher), 2)]
        
        plaintext = ""
        
        for pair in pairs:
            if len(pair) != 2:
                continue
                
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])
            
            if row1 is None or row2 is None:
                continue
                
            # Pravidlo 1: Stejný řádek (posun doleva)
            if row1 == row2:
                plaintext += self.table[row1][(col1 - 1) % 5]
                plaintext += self.table[row2][(col2 - 1) % 5]
            # Pravidlo 2: Stejný sloupec (posun nahoru)
            elif col1 == col2:
                plaintext += self.table[(row1 - 1) % 5][col1]
                plaintext += self.table[(row2 - 1) % 5][col2]
            # Pravidlo 3: Obdélník (záměna sloupců)
            else:
                plaintext += self.table[row1][col2]
                plaintext += self.table[row2][col1]
        
        # Obnovení mezer
        if spaces_pos is not None and padding_positions is not None:
            plaintext = self.restore_spaces_and_special(plaintext, spaces_pos, padding_positions)
        
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