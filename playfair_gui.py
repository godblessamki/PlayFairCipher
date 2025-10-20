import tkinter as tk
from tkinter import ttk, messagebox
import random

class PlayfairGUI:
    def __init__(self, root, cipher):
        self.root = root
        self.cipher = cipher
        self.root.title("🚀 CYBER PLAYFAIR ENCRYPTOR 9000 🚀")
        self.root.geometry("1200x900")
        self.root.configure(bg='#0a0a0a')
        
        # Moderní barevné schéma
        self.colors = {
            'bg': '#0a0a0a',
            'card_bg': '#1a1a1a',
            'accent': '#00ff88',
            'accent2': '#ff0088',
            'text': '#ffffff',
            'text_secondary': '#888888',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444'
        }
        
        self.setup_styles()
        self.setup_gui()
        self.start_animations()
        
    def setup_styles(self):
        """Vytvoří moderní styly pro widgety"""
        style = ttk.Style()
        
        # Konfigurace stylů
        style.configure('Cyber.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card_bg'], relief='raised', borderwidth=2)
        style.configure('Title.TLabel', background=self.colors['bg'], foreground=self.colors['accent'], 
                       font=('Consolas', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['card_bg'], foreground=self.colors['text'],
                       font=('Consolas', 12, 'bold'))
        style.configure('Normal.TLabel', background=self.colors['card_bg'], foreground=self.colors['text'],
                       font=('Consolas', 10))
        
        # Styly pro tlačítka
        style.configure('Cyber.TButton', background=self.colors['accent'], foreground='black',
                       font=('Consolas', 10, 'bold'), borderwidth=0, focuscolor='none')
        style.map('Cyber.TButton',
                 background=[('active', self.colors['accent2']),
                           ('pressed', self.colors['accent2'])])
        
        # Styly pro combobox
        style.configure('Cyber.TCombobox', fieldbackground=self.colors['card_bg'], background=self.colors['card_bg'],
                       foreground=self.colors['text'], selectbackground=self.colors['accent'])
        
        # Styly pro entry
        style.configure('Cyber.TEntry', fieldbackground=self.colors['card_bg'], foreground=self.colors['text'])
        
    def setup_gui(self):
        """Vytvoří ultra-moderní GUI"""
        # Hlavní kontejner
        main_container = ttk.Frame(self.root, style='Cyber.TFrame', padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header s animací
        self.header_frame = ttk.Frame(main_container, style='Cyber.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(self.header_frame, text="🔐 CYBER PLAYFAIR ENCRYPTOR 9000 🔐", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(self.header_frame, text=">> MILITARY GRADE ENCRYPTION TECHNOLOGY <<", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Hlavní obsah ve 2 sloupcích
        content_frame = ttk.Frame(main_container, style='Cyber.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Levý sloupec - ovládací prvky
        left_frame = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Pravý sloupec - tabulka a výstupy
        right_frame = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # === LEVÝ SLOUPEC ===
        self.setup_controls(left_frame)
        
        # === PRAVÝ SLOUPEC ===
        self.setup_outputs(right_frame)
        
        # Status bar
        self.setup_status_bar(main_container)
        
    def setup_controls(self, parent):
        """Nastaví ovládací prvky"""
        # Sekce konfigurace
        config_frame = ttk.LabelFrame(parent, text="⚙️ KONFIGURACE ŠIFRY", style='Subtitle.TLabel', padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Jazyk
        lang_frame = ttk.Frame(config_frame, style='Card.TFrame')
        lang_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lang_frame, text="JAZYK SYSTEMU:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="EN")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["EN", "CZ"], 
                                 state="readonly", width=8, style='Cyber.TCombobox')
        lang_combo.pack(side=tk.RIGHT, padx=(10, 0))
        lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Klíč
        key_frame = ttk.Frame(config_frame, style='Card.TFrame')
        key_frame.pack(fill=tk.X, pady=5)
        ttk.Label(key_frame, text="KÓDOVÉ SLOVO:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.key_var = tk.StringVar(value="PLAYFAIR")
        key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=20, style='Cyber.TEntry',
                             font=('Consolas', 10))
        key_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Tlačítko generování tabulky
        ttk.Button(config_frame, text="🔄 GENEROVAT ŠIFROVACÍ TABULKU", 
                  command=self.generate_table, style='Cyber.TButton').pack(fill=tk.X, pady=10)
        
        # Sekce textového vstupu
        input_frame = ttk.LabelFrame(parent, text="📥 VSTUPNÍ TEXT", style='Subtitle.TLabel', padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.input_text = tk.Text(input_frame, height=8, bg=self.colors['card_bg'], fg=self.colors['text'],
                                 insertbackground=self.colors['accent'], font=('Consolas', 10),
                                 relief='flat', borderwidth=2)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Tlačítka akcí
        button_frame = ttk.Frame(parent, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(button_frame, text="🚀 ŠIFROVAT", command=self.encrypt_text, 
                  style='Cyber.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(button_frame, text="🔓 DEŠIFROVAT", command=self.decrypt_text,
                  style='Cyber.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(button_frame, text="🧹 VYČISTIT", command=self.clear_text,
                  style='Cyber.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def setup_outputs(self, parent):
        """Nastaví výstupní prvky"""
        # Šifrovací tabulka
        table_frame = ttk.LabelFrame(parent, text="🔢 ŠIFROVACÍ TABULKA 5x5", style='Subtitle.TLabel', padding="10")
        table_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.table_container = ttk.Frame(table_frame, style='Card.TFrame')
        self.table_container.pack(fill=tk.X, pady=10)
        
        # Výstupní text
        output_frame = ttk.LabelFrame(parent, text="📤 VÝSTUPNÍ TEXT", style='Subtitle.TLabel', padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.output_text = tk.Text(output_frame, height=6, bg=self.colors['card_bg'], fg=self.colors['success'],
                                  insertbackground=self.colors['accent'], font=('Consolas', 10, 'bold'),
                                  relief='flat', borderwidth=2)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Detaily
        details_frame = ttk.LabelFrame(parent, text="📊 SYSTEM LOG", style='Subtitle.TLabel', padding="10")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(details_frame, height=8, bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                                   font=('Consolas', 8), relief='flat', borderwidth=2)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_status_bar(self, parent):
        """Nastaví status bar"""
        status_frame = ttk.Frame(parent, style='Card.TFrame', relief='sunken', borderwidth=1)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="🟢 SYSTEM READY - AWAITING ENCRYPTION COMMANDS")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Normal.TLabel',
                                font=('Consolas', 9))
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Přidání nějakých "systemových" indikátorů
        ttk.Label(status_frame, text="CPU: ████████  MEM: ████████  ENC: ACTIVE", 
                 style='Normal.TLabel', font=('Consolas', 8)).pack(side=tk.RIGHT, padx=5, pady=2)
    
    def start_animations(self):
        """Spustí animace pro futuristický vzhled"""
        self.animate_header()
        self.animate_status()
        
    def animate_header(self):
        """Animace headeru"""
        colors = ['#00ff88', '#ff0088', '#0088ff', '#ffff00']
        current_color = random.choice(colors)
        for widget in self.header_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(foreground=current_color)
        self.root.after(2000, self.animate_header)
    
    def animate_status(self):
        """Animace status baru"""
        status_messages = [
            "🟢 SYSTEM READY - AWAITING ENCRYPTION COMMANDS",
            "🔵 PROCESSING - ALGORITHMS ACTIVE",
            "🟣 SECURE CONNECTION ESTABLISHED",
            "🟠 OPTIMIZING CIPHER STRENGTH"
        ]
        current_msg = random.choice(status_messages)
        self.status_var.set(current_msg)
        self.root.after(3000, self.animate_status)
    
    def on_language_change(self, event=None):
        """Handle language change"""
        self.update_status(f"Language changed to: {self.lang_var.get()}")
        self.generate_table()
        
    def generate_table(self):
        """Generate and display the cipher table with animations"""
        try:
            key = self.key_var.get().strip()
            if not key:
                key = "PLAYFAIR"
                self.key_var.set(key)
            
            self.cipher.set_language(self.lang_var.get())
            self.cipher.generate_table(key)
            table = self.cipher.get_table()
            
            # Clear previous table
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Create animated table
            for i in range(5):
                for j in range(5):
                    cell = tk.Label(self.table_container, text=table[i][j], width=4, height=2,
                                  bg='#2a2a2a', fg=self.colors['accent'], font=('Consolas', 12, 'bold'),
                                  relief='raised', borderwidth=2)
                    cell.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                    # Animace při vytvoření
                    self.animate_cell(cell, i*100 + j*50)
            
            self.update_details(f"🔐 ŠIFROVACÍ TABULKA VYGENEROVÁNA\n"
                              f"🗝️  Klíč: {key}\n"
                              f"🌐 Jazyk: {self.lang_var.get()}\n"
                              f"📊 Velikost: 5x5\n"
                              f"✅ Systém připraven")
            
            self.update_status("🟢 Šifrovací tabulka úspěšně vygenerována")
            
        except Exception as e:
            self.update_status("🔴 Chyba při generování tabulky")
            messagebox.showerror("SYSTEM ERROR", f"CHYBA: {str(e)}")
    
    def animate_cell(self, cell, delay):
        """Animace buňky tabulky"""
        def animate():
            colors = ['#00ff88', '#ff0088', '#0088ff', '#2a2a2a']
            current_bg = cell.cget('bg')
            next_index = (colors.index(current_bg) + 1) % len(colors) if current_bg in colors else 0
            cell.configure(bg=colors[next_index])
            self.root.after(500, animate)
        
        self.root.after(delay, animate)
    
    def encrypt_text(self):
        """Encrypt the input text with style"""
        try:
            plaintext = self.input_text.get("1.0", tk.END).strip()
            if not plaintext:
                self.update_status("🟠 Varování: Zadejte text pro šifrování")
                messagebox.showwarning("INPUT REQUIRED", "ZADEJTE TEXT PRO ŠIFROVÁNÍ")
                return
            
            self.update_status("🟣 Probíhá šifrování...")
            self.root.update()
            
            ciphertext, bigramy, filtered, spaces, special = self.cipher.encrypt(plaintext)
            
            # Animovaný výstup
            self.output_text.delete("1.0", tk.END)
            self.typewriter_effect(self.output_text, ciphertext, 50)
            
            details = f"🚀 ŠIFROVÁNÍ ÚSPĚŠNÉ\n"
            details += f"📥 Původní text: {plaintext}\n"
            details += f"🔧 Filtrovaný text: {filtered}\n"
            details += f"🎯 Bigramy: {' '.join(bigramy)}\n"
            details += f"📤 Šifrovaný text: {ciphertext}\n"
            details += f"🔒 Šifrovací síla: EXCELLENT"
            
            self.update_details(details)
            self.update_status("🟢 Šifrování dokončeno")
            
        except Exception as e:
            self.update_status("🔴 Chyba při šifrování")
            messagebox.showerror("ENCRYPTION ERROR", f"CHYBA ŠIFROVÁNÍ: {str(e)}")
    
    def decrypt_text(self):
        """Decrypt the input text with style"""
        try:
            ciphertext = self.input_text.get("1.0", tk.END).strip()
            if not ciphertext:
                self.update_status("🟠 Varování: Zadejte text pro dešifrování")
                messagebox.showwarning("INPUT REQUIRED", "ZADEJTE TEXT PRO DEŠIFROVÁNÍ")
                return
            
            self.update_status("🟣 Probíhá dešifrování...")
            self.root.update()
            
            plaintext = self.cipher.decrypt(ciphertext)
            
            # Animovaný výstup
            self.output_text.delete("1.0", tk.END)
            self.typewriter_effect(self.output_text, plaintext, 30)
            
            details = f"🔓 DEŠIFROVÁNÍ ÚSPĚŠNÉ\n"
            details += f"📤 Šifrovaný text: {ciphertext}\n"
            details += f"📥 Dešifrovaný text: {plaintext}\n"
            details += f"✅ Integrita: VERIFIED\n"
            details += f"🔒 Zabezpečení: MAXIMUM"
            
            self.update_details(details)
            self.update_status("🟢 Dešifrování dokončeno")
            
        except Exception as e:
            self.update_status("🔴 Chyba při dešifrování")
            messagebox.showerror("DECRYPTION ERROR", f"CHYBA DEŠIFROVÁNÍ: {str(e)}")
    
    def typewriter_effect(self, text_widget, text, delay):
        """Efekt psacího stroje pro text"""
        def type_char(i=0):
            if i < len(text):
                text_widget.insert(tk.END, text[i])
                text_widget.see(tk.END)
                text_widget.after(delay, lambda: type_char(i+1))
        
        type_char()
    
    def clear_text(self):
        """Clear all text fields with animation"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.details_text.delete("1.0", tk.END)
        
        # Animace mazání
        self.output_text.insert("1.0", "🗑️ TEXT CLEARED")
        self.root.after(1000, lambda: self.output_text.delete("1.0", tk.END))
        
        self.update_status("🟡 Všechna pole vyčištěna")
        self.update_details("🧹 SYSTÉM VYČIŠTĚN\n✅ PŘIPRAVEN PRO NOVÉ ÚKOLY")
    
    def update_details(self, text):
        """Update details text area"""
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", text)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)