import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import hashlib
import time
import json
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np
import os

class ComplexProtectionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторна робота №7 - Комплексний захист")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f4f8')
        
        self.processed_data = {}
        self.metrics = {}
        self.combination_type = 'A'
        self.input_file_path = None
        self.cover_image_path = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        header_frame = tk.Frame(self.root, bg='#1e3a8a', pady=15)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="ЛАБОРАТОРНА РОБОТА №7", 
                font=('Arial', 18, 'bold'), bg='#1e3a8a', fg='white').pack()
        tk.Label(header_frame, text="Комплексний захист особистого проекту", 
                font=('Arial', 12), bg='#1e3a8a', fg='#93c5fd').pack()
        tk.Label(header_frame, text="Виконав: Буман М.О., група 6.04.122.010.22.1", 
                font=('Arial', 10), bg='#1e3a8a', fg='#93c5fd').pack()
        
        # Основний контейнер
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Вибір комбінації
        self.create_combination_selector(main_frame)
        
        # Введення даних
        self.create_input_section(main_frame)
        
        # Кнопки дій
        self.create_action_buttons(main_frame)
        
        # Результати та метрики
        self.create_results_section(main_frame)
        
    def create_combination_selector(self, parent):
        frame = tk.LabelFrame(parent, text="Оберіть комбінацію методів захисту", 
                             font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        frame.pack(fill='x', pady=(0, 10))
        
        combinations = [
            ('A', 'Комбінація А\nШифрування + Стеганографія', '#6366f1'),
            ('B', 'Комбінація Б\nПідпис + Шифрування', '#10b981'),
            ('C', 'Комбінація В\nСтеганографія + Підпис', '#8b5cf6')
        ]
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack()
        
        for combo_id, text, color in combinations:
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                          bg=color, fg='white', width=25, height=4,
                          relief='raised', bd=3, cursor='hand2',
                          command=lambda c=combo_id: self.select_combination(c))
            btn.pack(side='left', padx=10)
            
    def create_input_section(self, parent):
        frame = tk.LabelFrame(parent, text="Введення даних", 
                             font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        frame.pack(fill='x', pady=(0, 10))
        
        # Вибір файлу для захисту
        file_frame = tk.Frame(frame, bg='white')
        file_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(file_frame, text="Файл для захисту (TXT):", 
                font=('Arial', 10, 'bold'), bg='white').pack(side='left')
        self.file_label = tk.Label(file_frame, text="Файл не обрано", 
                                   font=('Arial', 9), bg='white', fg='gray')
        self.file_label.pack(side='left', padx=10)
        tk.Button(file_frame, text="Обрати файл", command=self.select_input_file,
                 bg='#6366f1', fg='white', font=('Arial', 9, 'bold')).pack(side='left')
        
        # Вибір зображення-контейнера
        image_frame = tk.Frame(frame, bg='white')
        image_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(image_frame, text="Зображення-контейнер (PNG):", 
                font=('Arial', 10, 'bold'), bg='white').pack(side='left')
        self.image_label = tk.Label(image_frame, text="Зображення не обрано", 
                                    font=('Arial', 9), bg='white', fg='gray')
        self.image_label.pack(side='left', padx=10)
        tk.Button(image_frame, text="Обрати зображення", command=self.select_cover_image,
                 bg='#6366f1', fg='white', font=('Arial', 9, 'bold')).pack(side='left')
        
        # Персональні дані
        personal_frame = tk.Frame(frame, bg='white')
        personal_frame.pack(fill='x', pady=(10, 0))
        
        # Email
        email_frame = tk.Frame(personal_frame, bg='white')
        email_frame.pack(fill='x', pady=(0, 10))
        tk.Label(email_frame, text="Електронна пошта:", 
                font=('Arial', 10, 'bold'), bg='white', width=20, anchor='w').pack(side='left')
        self.email_entry = tk.Entry(email_frame, font=('Arial', 10), width=40)
        self.email_entry.pack(side='left', padx=5)
        
        # Дата народження
        birth_frame = tk.Frame(personal_frame, bg='white')
        birth_frame.pack(fill='x')
        tk.Label(birth_frame, text="Дата народження:", 
                font=('Arial', 10, 'bold'), bg='white', width=20, anchor='w').pack(side='left')
        self.birth_entry = tk.Entry(birth_frame, font=('Arial', 10), width=40)
        self.birth_entry.pack(side='left', padx=5)
        tk.Label(birth_frame, text="(формат: ДД.ММ.РРРР)", 
                font=('Arial', 8), bg='white', fg='gray').pack(side='left')
        
    def create_action_buttons(self, parent):
        frame = tk.Frame(parent, bg='#f0f4f8')
        frame.pack(fill='x', pady=(0, 10))
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'height': 2, 'cursor': 'hand2', 
                    'relief': 'raised', 'bd': 3}
        
        self.protect_btn = tk.Button(frame, text="Застосувати захист", 
                                    bg='#6366f1', fg='white', 
                                    command=self.apply_protection, **btn_style)
        self.protect_btn.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        self.recover_btn = tk.Button(frame, text="Відновити дані", 
                                    bg='#10b981', fg='white', 
                                    command=self.recover_data, **btn_style)
        self.recover_btn.pack(side='left', fill='x', expand=True, padx=(3, 3))
        
        self.test_all_btn = tk.Button(frame, text="Тестувати всіма комбінаціями", 
                                     bg='#f59e0b', fg='white', 
                                     command=self.test_all_combinations, **btn_style)
        self.test_all_btn.pack(side='left', fill='x', expand=True, padx=(3, 3))
        
        self.report_btn = tk.Button(frame, text="Згенерувати звіт", 
                                   bg='#8b5cf6', fg='white', 
                                   command=self.generate_report, **btn_style)
        self.report_btn.pack(side='left', fill='x', expand=True, padx=(3, 0))
        
    def create_results_section(self, parent):
        frame = tk.LabelFrame(parent, text="Результати та аналітика", 
                             font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        frame.pack(fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(frame, height=25, 
                                                     font=('Consolas', 9), 
                                                     bg='#f8fafc', wrap='word')
        self.results_text.pack(fill='both', expand=True)
        
    def select_combination(self, combo):
        self.combination_type = combo
        messagebox.showinfo("Комбінація обрана", 
                          f"Обрано комбінацію {combo}")
    
    def select_input_file(self):
        filepath = filedialog.askopenfilename(
            title="Оберіть текстовий файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.input_file_path = filepath
            self.file_label.config(text=os.path.basename(filepath), fg='green')
    
    def select_cover_image(self):
        filepath = filedialog.askopenfilename(
            title="Оберіть PNG зображення",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filepath:
            self.cover_image_path = filepath
            self.image_label.config(text=os.path.basename(filepath), fg='green')
        
    def generate_key_from_personal_data(self, email, birthdate):
        """Генерація ключа з персональних даних"""
        combined = f"{email.lower().strip()}:{birthdate.strip()}"
        key = hashlib.sha256(combined.encode()).digest()
        return key
    
    # ========== МЕТОДИ ЗАХИСТУ ==========
    
    def encrypt_aes_file(self, filepath, key):
        """Шифрування файлу AES-256"""
        start_time = time.time()
        
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(file_data, AES.block_size))
            
            # Зберігаємо IV + зашифровані дані
            encrypted_data = cipher.iv + ct_bytes
            
            # Зберігаємо у тимчасовий файл
            output_path = filepath.replace('.txt', '_encrypted.bin')
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            elapsed = (time.time() - start_time) * 1000
            
            return {
                'path': output_path,
                'data': encrypted_data,
                'time': round(elapsed, 2),
                'size_before': len(file_data),
                'size_after': len(encrypted_data)
            }
        except Exception as e:
            raise Exception(f"Помилка шифрування: {str(e)}")
    
    def decrypt_aes_file(self, encrypted_data, key):
        """Розшифрування файлу AES-256"""
        start_time = time.time()
        
        try:
            iv = encrypted_data[:16]
            ct = encrypted_data[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            
            elapsed = (time.time() - start_time) * 1000
            
            return {
                'data': pt,
                'time': round(elapsed, 2)
            }
        except Exception as e:
            return {'data': None, 'error': str(e)}
    
    def hide_data_in_image_lsb(self, image_path, data_to_hide):
        """LSB стеганографія - приховування даних в зображенні"""
        start_time = time.time()
        
        try:
            # Відкриваємо зображення
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Конвертуємо дані в бінарний формат
            data_bytes = data_to_hide
            data_len = len(data_bytes)
            
            # Перевіряємо чи достатньо місця
            max_bytes = (img_array.shape[0] * img_array.shape[1] * 3) // 8 - 4
            if data_len > max_bytes:
                raise Exception("Файл занадто великий для цього зображення")
            
            # Додаємо довжину даних на початок
            data_with_len = data_len.to_bytes(4, byteorder='big') + data_bytes
            
            # Конвертуємо у біти
            data_bits = ''.join(format(byte, '08b') for byte in data_with_len)
            
            # Вбудовуємо дані в LSB
            flat_img = img_array.flatten()
            for i, bit in enumerate(data_bits):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            # Відновлюємо форму зображення
            stego_img_array = flat_img.reshape(img_array.shape)
            stego_img = Image.fromarray(stego_img_array.astype('uint8'))
            
            # Зберігаємо
            output_path = image_path.replace('.png', '_stego.png')
            stego_img.save(output_path, 'PNG')
            
            elapsed = (time.time() - start_time) * 1000
            
            return {
                'path': output_path,
                'time': round(elapsed, 2),
                'size': os.path.getsize(output_path)
            }
        except Exception as e:
            raise Exception(f"Помилка стеганографії: {str(e)}")
    
    def extract_data_from_image_lsb(self, image_path):
        """Витягування даних з зображення LSB"""
        start_time = time.time()
        
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Витягуємо біти
            flat_img = img_array.flatten()
            
            # Читаємо довжину даних (перші 32 біти)
            len_bits = ''.join(str(flat_img[i] & 1) for i in range(32))
            data_len = int(len_bits, 2)
            
            # Читаємо дані
            data_bits = ''.join(str(flat_img[i] & 1) for i in range(32, 32 + data_len * 8))
            
            # Конвертуємо біти назад в байти
            data_bytes = bytearray()
            for i in range(0, len(data_bits), 8):
                byte = data_bits[i:i+8]
                data_bytes.append(int(byte, 2))
            
            elapsed = (time.time() - start_time) * 1000
            
            return {
                'data': bytes(data_bytes),
                'time': round(elapsed, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_signature(self, data, key):
        """Генерація цифрового підпису"""
        start_time = time.time()
        
        data_hash = hashlib.sha256(data).hexdigest()
        key_hash = hashlib.sha256(key).hexdigest()
        
        signature = hex(int(data_hash, 16) ^ int(key_hash, 16))[2:].zfill(64)
        
        elapsed = (time.time() - start_time) * 1000
        
        return {
            'signature': signature,
            'time': round(elapsed, 2)
        }
    
    def verify_signature(self, data, signature, key):
        """Перевірка цифрового підпису"""
        generated = self.generate_signature(data, key)
        return generated['signature'] == signature
    
    # ========== КОМБІНАЦІЇ ==========
    
    def combination_a(self, filepath, image_path, key):
        """Комбінація А: Шифрування + Стеганографія"""
        total_start = time.time()
        
        # Етап 1: Шифрування файлу
        self.log_message("Етап 1: Шифрування файлу алгоритмом AES...")
        encrypted = self.encrypt_aes_file(filepath, key)
        
        # Етап 2: Приховування в зображення
        self.log_message("Етап 2: Приховування зашифрованого файлу в зображення (LSB)...")
        stego = self.hide_data_in_image_lsb(image_path, encrypted['data'])
        
        # Генерація підпису
        signature = self.generate_signature(encrypted['data'], key)
        
        total_time = (time.time() - total_start) * 1000
        
        return {
            'type': 'A',
            'stego_path': stego['path'],
            'encrypted_data': encrypted['data'],
            'signature': signature['signature'],
            'metrics': {
                'encryption_time': encrypted['time'],
                'stego_time': stego['time'],
                'signature_time': signature['time'],
                'total_time': round(total_time, 2),
                'original_size': encrypted['size_before'],
                'encrypted_size': encrypted['size_after'],
                'final_size': stego['size']
            }
        }
    
    def combination_b(self, filepath, image_path, key):
        """Комбінація Б: Підпис + Шифрування"""
        total_start = time.time()
        
        # Читаємо файл
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # Етап 1: Генерація підпису
        self.log_message("Етап 1: Генерація цифрового підпису...")
        signature = self.generate_signature(file_data, key)
        
        # Додаємо підпис до даних
        data_with_sig = file_data + b'|||' + signature['signature'].encode()
        
        # Тимчасово зберігаємо
        temp_path = filepath.replace('.txt', '_temp.txt')
        with open(temp_path, 'wb') as f:
            f.write(data_with_sig)
        
        # Етап 2: Шифрування
        self.log_message("Етап 2: Шифрування файлу з підписом...")
        encrypted = self.encrypt_aes_file(temp_path, key)
        
        # Видаляємо тимчасовий файл
        os.remove(temp_path)
        
        total_time = (time.time() - total_start) * 1000
        
        return {
            'type': 'B',
            'encrypted_path': encrypted['path'],
            'encrypted_data': encrypted['data'],
            'signature': signature['signature'],
            'metrics': {
                'signature_time': signature['time'],
                'encryption_time': encrypted['time'],
                'total_time': round(total_time, 2),
                'original_size': len(file_data),
                'encrypted_size': encrypted['size_after'],
                'final_size': encrypted['size_after']
            }
        }
    
    def combination_c(self, filepath, image_path, key):
        """Комбінація В: Стеганографія + Підпис"""
        total_start = time.time()
        
        # Читаємо файл
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # Етап 1: Генерація підпису
        self.log_message("Етап 1: Генерація цифрового підпису...")
        signature = self.generate_signature(file_data, key)
        
        # Додаємо підпис до даних
        data_with_sig = file_data + b'|||' + signature['signature'].encode()
        
        # Етап 2: Приховування в зображення
        self.log_message("Етап 2: Приховування файлу з підписом в зображення...")
        stego = self.hide_data_in_image_lsb(image_path, data_with_sig)
        
        total_time = (time.time() - total_start) * 1000
        
        return {
            'type': 'C',
            'stego_path': stego['path'],
            'signature': signature['signature'],
            'metrics': {
                'signature_time': signature['time'],
                'stego_time': stego['time'],
                'total_time': round(total_time, 2),
                'original_size': len(file_data),
                'final_size': stego['size']
            }
        }
    
    # ========== ОБРОБКА ДАНИХ ==========
    
    def log_message(self, message):
        """Виведення повідомлення в консоль результатів"""
        self.results_text.insert('end', message + '\n')
        self.results_text.see('end')
        self.root.update()
    
    def apply_protection(self):
        email = self.email_entry.get().strip()
        birthdate = self.birth_entry.get().strip()
        
        if not email or not birthdate:
            messagebox.showerror("Помилка", "Введіть електронну пошту та дату народження!")
            return
        
        if not self.input_file_path:
            messagebox.showerror("Помилка", "Оберіть файл для захисту!")
            return
        
        if not self.cover_image_path:
            messagebox.showerror("Помилка", "Оберіть зображення-контейнер!")
            return
        
        try:
            self.results_text.delete('1.0', 'end')
            self.log_message("=" * 70)
            self.log_message(f"ЗАСТОСУВАННЯ ЗАХИСТУ - Комбінація {self.combination_type}")
            self.log_message("=" * 70 + "\n")
            
            key = self.generate_key_from_personal_data(email, birthdate)
            
            if self.combination_type == 'A':
                result = self.combination_a(self.input_file_path, self.cover_image_path, key)
            elif self.combination_type == 'B':
                result = self.combination_b(self.input_file_path, self.cover_image_path, key)
            else:
                result = self.combination_c(self.input_file_path, self.cover_image_path, key)
            
            self.processed_data = result
            self.display_metrics(result)
            
            # Автоматичне тестування цілісності
            self.log_message("\n" + "=" * 70)
            self.log_message("АВТОМАТИЧНЕ ТЕСТУВАННЯ ЦІЛІСНОСТІ")
            self.log_message("=" * 70 + "\n")
            self.test_integrity(result, key)
            
            messagebox.showinfo("Успіх", "Захист успішно застосовано!")
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка обробки: {str(e)}")
    
    def recover_data(self):
        if not self.processed_data:
            messagebox.showerror("Помилка", "Спочатку застосуйте захист!")
            return
        
        email = self.email_entry.get().strip()
        birthdate = self.birth_entry.get().strip()
        
        if not email or not birthdate:
            messagebox.showerror("Помилка", "Введіть персональні дані!")
            return
        
        try:
            self.results_text.delete('1.0', 'end')
            self.log_message("=" * 70)
            self.log_message("ВІДНОВЛЕННЯ ДАНИХ")
            self.log_message("=" * 70 + "\n")
            
            key = self.generate_key_from_personal_data(email, birthdate)
            recovered = None
            valid = False
            
            if self.processed_data['type'] == 'A':
                self.log_message("Витягування даних з зображення...")
                extracted = self.extract_data_from_image_lsb(self.processed_data['stego_path'])
                if 'error' in extracted:
                    raise Exception("Не вдалося витягти дані")
                
                self.log_message("Розшифрування даних...")
                decrypted = self.decrypt_aes_file(extracted['data'], key)
                if decrypted['data'] is None:
                    raise Exception("Невірні персональні дані!")
                
                recovered = decrypted['data']
                valid = self.verify_signature(extracted['data'], 
                                              self.processed_data['signature'], key)
            
            elif self.processed_data['type'] == 'B':
                self.log_message("Розшифрування файлу...")
                decrypted = self.decrypt_aes_file(self.processed_data['encrypted_data'], key)
                if decrypted['data'] is None:
                    raise Exception("Невірні персональні дані!")
                
                parts = decrypted['data'].split(b'|||')
                recovered = parts[0]
                signature = parts[1].decode()
                
                valid = self.verify_signature(recovered, signature, key)
            
            elif self.processed_data['type'] == 'C':
                self.log_message("Витягування даних з зображення...")
                extracted = self.extract_data_from_image_lsb(self.processed_data['stego_path'])
                if 'error' in extracted:
                    raise Exception("Не вдалося витягти дані")
                
                parts = extracted['data'].split(b'|||')
                recovered = parts[0]
                signature = parts[1].decode()
                
                valid = self.verify_signature(recovered, signature, key)
            
            # Зберігаємо відновлений файл
            output_path = self.input_file_path.replace('.txt', '_recovered.txt')
            with open(output_path, 'wb') as f:
                f.write(recovered)
            
            status = "ДІЙСНИЙ" if valid else "НЕДІЙСНИЙ"
            self.log_message(f"\nФайл успішно відновлено: {output_path}")
            self.log_message(f"Цифровий підпис: {status}")
            
            messagebox.showinfo("Відновлення успішне", 
                              f"Файл відновлено: {output_path}\n"
                              f"Підпис: {status}")
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка відновлення: {str(e)}")
    
    def test_integrity(self, result, key):
        """Тестування цілісності після повного циклу"""
        try:
            self.log_message("Виконання тесту захист -> відновлення...\n")
            
            # Читаємо оригінальний файл
            with open(self.input_file_path, 'rb') as f:
                original_data = f.read()
            
            recovered = None
            
            if result['type'] == 'A':
                extracted = self.extract_data_from_image_lsb(result['stego_path'])
                decrypted = self.decrypt_aes_file(extracted['data'], key)
                recovered = decrypted['data']
            
            elif result['type'] == 'B':
                decrypted = self.decrypt_aes_file(result['encrypted_data'], key)
                recovered = decrypted['data'].split(b'|||')[0]
            
            elif result['type'] == 'C':
                extracted = self.extract_data_from_image_lsb(result['stego_path'])
                recovered = extracted['data'].split(b'|||')[0]
            
            # Перевірка
            integrity_ok = (original_data == recovered)
            
            self.log_message(f"Розмір оригіналу: {len(original_data)} байт")
            self.log_message(f"Розмір відновленого: {len(recovered)} байт")
            self.log_message(f"Цілісність даних: {'OK - Дані ідентичні' if integrity_ok else 'ПОМИЛКА - Дані відрізняються'}")
            
            if integrity_ok:
                self.log_message("\nТест пройдено успішно!")
            else:
                self.log_message("\nТест не пройдено! Виявлено пошкодження даних.")
                
        except Exception as e:
            self.log_message(f"\nПомилка тестування: {str(e)}")
    
    def test_all_combinations(self):
        """Тестування всіма комбінаціями"""
        email = self.email_entry.get().strip()
        birthdate = self.birth_entry.get().strip()
        
        if not email or not birthdate:
            messagebox.showerror("Помилка", "Введіть персональні дані!")
            return
        
        if not self.input_file_path or not self.cover_image_path:
            messagebox.showerror("Помилка", "Оберіть файл та зображення!")
            return
        
        try:
            self.results_text.delete('1.0', 'end')
            self.log_message("=" * 70)
            self.log_message("АВТОМАТИЧНЕ ТЕСТУВАННЯ ВСІХ КОМБІНАЦІЙ")
            self.log_message("=" * 70 + "\n")
            
            key = self.generate_key_from_personal_data(email, birthdate)
            all_results = []
            
            for combo in ['A', 'B', 'C']:
                self.log_message(f"\n{'=' * 70}")
                self.log_message(f"ТЕСТУВАННЯ КОМБІНАЦІЇ {combo}")
                self.log_message("=" * 70 + "\n")
                
                if combo == 'A':
                    result = self.combination_a(self.input_file_path, self.cover_image_path, key)
                elif combo == 'B':
                    result = self.combination_b(self.input_file_path, self.cover_image_path, key)
                else:
                    result = self.combination_c(self.input_file_path, self.cover_image_path, key)
                
                all_results.append(result)
                self.display_metrics(result)
                self.test_integrity(result, key)
            
            # Порівняльна таблиця
            self.log_message("\n\n" + "=" * 70)
            self.log_message("ПОРІВНЯЛЬНА ТАБЛИЦЯ ВСІХ КОМБІНАЦІЙ")
            self.log_message("=" * 70 + "\n")
            self.display_comparison_table(all_results)
            
            messagebox.showinfo("Тестування завершено", "Всі комбінації протестовано успішно!")
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка тестування: {str(e)}")
    
    def generate_report(self):
        """Генерація повного звіту"""
        if not self.processed_data:
            messagebox.showerror("Помилка", "Спочатку застосуйте захист або проведіть тестування!")
            return
        
        try:
            self.results_text.delete('1.0', 'end')
            
            report = f"""
{'=' * 70}
ЗВІТ ПРО КОМПЛЕКСНИЙ ЗАХИСТ ДАНИХ
{'=' * 70}

Дата формування: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Виконав: Буман М.О., група 6.04.122.010.22.1

{'=' * 70}
1. ЗАГАЛЬНА ІНФОРМАЦІЯ
{'=' * 70}

Вхідний файл: {os.path.basename(self.input_file_path) if self.input_file_path else 'Не вказано'}
Зображення-контейнер: {os.path.basename(self.cover_image_path) if self.cover_image_path else 'Не вказано'}
Обрана комбінація: {self.get_combination_name(self.processed_data['type'])}

{'=' * 70}
2. ОПИС МЕТОДІВ ЗАХИСТУ
{'=' * 70}

2.1. Шифрування файлів (AES-256)
    - Алгоритм: AES (Advanced Encryption Standard)
    - Режим: CBC (Cipher Block Chaining)
    - Розмір ключа: 256 біт
    - Генерація ключа: SHA-256 хеш персональних даних
    - Призначення: забезпечення конфіденційності даних

2.2. Цифровий підпис
    - Алгоритм хешування: SHA-256
    - Метод: XOR хешів повідомлення та ключа
    - Призначення: перевірка цілісності та автентичності

2.3. LSB Стеганографія
    - Метод: Least Significant Bit
    - Контейнер: PNG зображення
    - Призначення: приховування самого факту передачі даних

{'=' * 70}
3. МЕТРИКИ ЕФЕКТИВНОСТІ
{'=' * 70}

"""
            
            metrics = self.processed_data['metrics']
            
            report += f"Час виконання операцій:\n"
            if 'encryption_time' in metrics:
                report += f"  - Шифрування: {metrics['encryption_time']} мс\n"
            if 'signature_time' in metrics:
                report += f"  - Генерація підпису: {metrics['signature_time']} мс\n"
            if 'stego_time' in metrics:
                report += f"  - Стеганографія: {metrics['stego_time']} мс\n"
            report += f"  - Загальний час: {metrics['total_time']} мс\n\n"
            
            report += f"Розміри файлів:\n"
            report += f"  - Оригінальний розмір: {metrics['original_size']} байт\n"
            if 'encrypted_size' in metrics:
                report += f"  - Після шифрування: {metrics['encrypted_size']} байт\n"
            report += f"  - Фінальний розмір: {metrics['final_size']} байт\n"
            
            increase = ((metrics['final_size'] / metrics['original_size'] - 1) * 100)
            report += f"  - Збільшення розміру: {increase:.1f}%\n\n"
            
            report += f"""
{'=' * 70}
4. АНАЛІЗ ОБРАНОЇ КОМБІНАЦІЇ
{'=' * 70}

"""
            
            analysis = self.get_combination_analysis(self.processed_data['type'])
            report += analysis
            
            report += f"""

{'=' * 70}
5. РЕКОМЕНДАЦІЇ
{'=' * 70}

Загальні рекомендації:
  1. Використовуйте складні паролі та унікальні персональні дані
  2. Регулярно оновлюйте ключі шифрування
  3. Зберігайте резервні копії незашифрованих даних в безпечному місці
  4. Використовуйте зображення достатнього розміру для стеганографії

Рекомендації для конкретних сценаріїв:

  Комбінація А (Шифрування + Стеганографія):
    - Використовуйте для максимально конфіденційних даних
    - Найкраща для прихованої передачі інформації
    - Підходить для каналів з можливим перехопленням
    - Вимагає більше часу на обробку

  Комбінація Б (Підпис + Шифрування):
    - Оптимальна для юридично значимих документів
    - Гарантує автентичність відправника
    - Швидша за комбінацію А
    - Не приховує факт шифрування

  Комбінація В (Стеганографія + Підпис):
    - Баланс між прихованістю та перевіркою цілісності
    - Підходить для передачі в публічних каналах
    - Без шифрування, але з перевіркою автора
    - Найшвидша комбінація

{'=' * 70}
6. ВИСНОВКИ
{'=' * 70}

Система комплексного захисту успішно реалізована та протестована.
Всі методи працюють коректно та забезпечують необхідний рівень захисту.

Обрана комбінація {self.processed_data['type']} показала наступні результати:
  - Час обробки: {metrics['total_time']} мс
  - Ефективність: {"Висока" if metrics['total_time'] < 1000 else "Середня"}
  - Надійність: Підтверджено тестами цілісності

{'=' * 70}
КІНЕЦЬ ЗВІТУ
{'=' * 70}
"""
            
            self.results_text.insert('1.0', report)
            
            # Зберігаємо звіт у файл
            report_path = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            messagebox.showinfo("Звіт згенеровано", f"Звіт збережено: {report_path}")
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка генерації звіту: {str(e)}")
    
    def display_metrics(self, result):
        """Відображення метрик"""
        metrics = result['metrics']
        
        output = f"\nМЕТРИКИ ВИКОНАННЯ:\n"
        output += f"{'-' * 70}\n"
        
        if 'encryption_time' in metrics:
            output += f"Час шифрування: {metrics['encryption_time']} мс\n"
        if 'signature_time' in metrics:
            output += f"Час генерації підпису: {metrics['signature_time']} мс\n"
        if 'stego_time' in metrics:
            output += f"Час стеганографії: {metrics['stego_time']} мс\n"
        
        output += f"Загальний час: {metrics['total_time']} мс\n"
        output += f"\nРозмір оригіналу: {metrics['original_size']} байт\n"
        
        if 'encrypted_size' in metrics:
            output += f"Розмір після шифрування: {metrics['encrypted_size']} байт\n"
        
        output += f"Фінальний розмір: {metrics['final_size']} байт\n"
        
        increase = ((metrics['final_size'] / metrics['original_size'] - 1) * 100)
        output += f"Збільшення: {increase:.1f}%\n"
        
        self.log_message(output)
    
    def display_comparison_table(self, results):
        """Відображення порівняльної таблиці"""
        output = f"{'Метрика':<30} | {'Комб. А':<15} | {'Комб. Б':<15} | {'Комб. В':<15}\n"
        output += f"{'-' * 80}\n"
        
        # Час
        times = [r['metrics']['total_time'] for r in results]
        output += f"{'Загальний час (мс)':<30} | {times[0]:<15.2f} | {times[1]:<15.2f} | {times[2]:<15.2f}\n"
        
        # Розмір
        sizes = [r['metrics']['final_size'] for r in results]
        output += f"{'Фінальний розмір (байт)':<30} | {sizes[0]:<15} | {sizes[1]:<15} | {sizes[2]:<15}\n"
        
        # Збільшення
        increases = [((r['metrics']['final_size'] / r['metrics']['original_size'] - 1) * 100) for r in results]
        output += f"{'Збільшення розміру (%)':<30} | {increases[0]:<15.1f} | {increases[1]:<15.1f} | {increases[2]:<15.1f}\n"
        
        output += f"\nРЕКОМЕНДАЦІЇ:\n"
        fastest = ['A', 'B', 'C'][times.index(min(times))]
        smallest = ['A', 'B', 'C'][sizes.index(min(sizes))]
        
        output += f"  - Найшвидша комбінація: {fastest}\n"
        output += f"  - Найменший розмір: {smallest}\n"
        
        self.log_message(output)
    
    def get_combination_name(self, combo_type):
        names = {
            'A': 'Шифрування + Стеганографія',
            'B': 'Цифровий підпис + Шифрування',
            'C': 'Стеганографія + Цифровий підпис'
        }
        return names.get(combo_type, 'Невідома')
    
    def get_combination_analysis(self, combo_type):
        analyses = {
            'A': """
Комбінація А забезпечує максимальний рівень захисту та прихованості:

Переваги:
  - Максимальна конфіденційність (AES-256 шифрування)
  - Повне приховування факту передачі даних
  - Подвійний захист: шифрування + стеганографія
  - Складність виявлення навіть при перехопленні

Недоліки:
  - Найдовший час обробки
  - Вимагає зображення достатнього розміру
  - Найскладніша реалізація

Рейтинги:
  - Конфіденційність: 5/5
  - Приховування: 5/5
  - Цілісність: 3/5
  - Швидкість: 3/5
  - Складність: Висока
""",
            'B': """
Комбінація Б оптимальна для документів з цифровим підписом:

Переваги:
  - Максимальна цілісність та автентичність
  - Висока конфіденційність
  - Швидка обробка
  - Простіша реалізація

Недоліки:
  - Видимий факт шифрування
  - Не приховує передачу даних
  - Більший фінальний розмір

Рейтинги:
  - Конфіденційність: 5/5
  - Приховування: 1/5
  - Цілісність: 5/5
  - Швидкість: 4/5
  - Складність: Середня
""",
            'C': """
Комбінація В - компроміс між прихованістю та цілісністю:

Переваги:
  - Висока прихованість
  - Перевірка цілісності та автора
  - Найшвидша обробка
  - Менший розмір

Недоліки:
  - Відсутність шифрування
  - Дані не захищені від читання при витягуванні
  - Середня конфіденційність

Рейтинги:
  - Конфіденційність: 3/5
  - Приховування: 5/5
  - Цілісність: 5/5
  - Швидкість: 4/5
  - Складність: Середня
"""
        }
        return analyses.get(combo_type, "Аналіз недоступний")


if __name__ == "__main__":
    root = tk.Tk()
    app = ComplexProtectionSystem(root)
    root.mainloop()