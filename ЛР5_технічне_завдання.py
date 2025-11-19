import tkinter as tk
from tkinter import messagebox
from hashlib import sha256
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import re

# Функції 
def generate_key(email, birthdate):

    email = (email or "").strip()
    birth = (birthdate or "").strip()

    local = email.split("@")[0] if "@" in email else email

    segments = re.findall(r"[A-Za-zА-Яа-яІіЇїЄєҐґ]+", local)

    segments = [s for s in segments if len(s) > 1]

    if segments:
        personal = "".join(s.capitalize() for s in segments)

        key_display = personal + birth
        data = key_display
    else:
    
        key_display = email + birth
        data = key_display

    # SHA-256 → 32 байти
    key_bytes = sha256(data.encode("utf-8")).digest()
    return key_bytes, key_display


def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    return f"{iv}:{ct}"


def decrypt_message(enc_message, key):
    try:
        iv_str, ct_str = enc_message.split(":")
        iv = b64decode(iv_str)
        ct = b64decode(ct_str)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode("utf-8")
    except Exception as e:
        return f"Помилка розшифрування: {e}"


class EmailEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифратор")
        self.root.geometry("800x450")

        # Email і Дата народження
        frame1 = tk.Frame(root)
        frame1.pack(pady=5, fill="x", padx=10)

        tk.Label(frame1, text="Email:").pack(side="left")
        self.entry_email = tk.Entry(frame1, width=35)
        self.entry_email.pack(side="left", padx=5)

        tk.Label(frame1, text="Дата народження (ДДММРРРР):").pack(side="left")
        self.entry_birth = tk.Entry(frame1, width=12)
        self.entry_birth.pack(side="left", padx=5)

        # Повідомлення 
        frame2 = tk.Frame(root)
        frame2.pack(pady=5, fill="x", padx=10)

        tk.Label(frame2, text="Повідомлення:").pack(side="left")
        self.entry_message = tk.Entry(frame2, width=60)
        self.entry_message.pack(side="left", padx=5)

        # Поле для ключа
        frame_key = tk.Frame(root)
        frame_key.pack(fill="x", padx=10)
        self.label_key = tk.Label(frame_key, text="Ключ: ", fg="blue")
        self.label_key.pack(anchor="w", pady=5)

        # Рядок: Кнопки 
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Генерувати ключ", command=self.generate_key_gui).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Зашифрувати", command=self.encrypt_gui).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Розшифрувати", command=self.decrypt_gui).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Тестовий приклад", command=self.test_example).pack(side="left", padx=5)

        # Поле результату
        tk.Label(root, text="Результат:").pack()
        self.text_result = tk.Text(root, height=12)
        self.text_result.pack(fill="x", padx=10)

        self.key = None
        self.key_display = ""
        self.enc_message = None

    # Логіка кнопок 
    def generate_key_gui(self):
        email = self.entry_email.get().strip()
        birth = self.entry_birth.get().strip()
        if not email or not birth:
            messagebox.showerror("Помилка", "Введіть Email та дату народження")
            return

        self.key, self.key_display = generate_key(email, birth)
        self.label_key.config(text=f"Ключ: {self.key_display}")
        messagebox.showinfo("Успіх", "Симетричний ключ згенеровано!")

    def encrypt_gui(self):
        if not self.key:
            messagebox.showerror("Помилка", "Спочатку згенеруйте ключ")
            return
        message = self.entry_message.get().strip()
        if not message:
            messagebox.showerror("Помилка", "Введіть повідомлення")
            return
        self.enc_message = encrypt_message(message, self.key)
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, self.enc_message)

    def decrypt_gui(self):
        if not self.key:
            messagebox.showerror("Помилка", "Спочатку згенеруйте ключ")
            return
        if not self.enc_message:
            messagebox.showerror("Помилка", "Спочатку зашифруйте повідомлення")
            return
        dec_message = decrypt_message(self.enc_message, self.key)
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, dec_message)

    def test_example(self):
        email = "ivan.petrenko@gmail.com"
        birth = "1995"
        message = "Зустрічаємося завтра о 15:00"

        # Встановлюємо поля
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, email)
        self.entry_birth.delete(0, tk.END)
        self.entry_birth.insert(0, birth)
        self.entry_message.delete(0, tk.END)
        self.entry_message.insert(0, message)

        # Генеруємо ключ і шифруємо
        self.key, self.key_display = generate_key(email, birth)
        self.label_key.config(text=f"Ключ: {self.key_display}")
        self.enc_message = encrypt_message(message, self.key)

        # Результат
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, f"Зашифроване повідомлення:\n{self.enc_message}\n\n")
        dec_message = decrypt_message(self.enc_message, self.key)
        self.text_result.insert(tk.END, f"Розшифроване повідомлення:\n{dec_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailEncryptorApp(root)
    root.mainloop()
