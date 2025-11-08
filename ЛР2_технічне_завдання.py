# Порівняльний аналіз класичних шифрів
# Підтримує: Caesar, Vigenere, Atbash
# Запуск: python cipher_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog

# Український алфавіт (33 літери)
UK_ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
UK_ALPHABET_LOWER = UK_ALPHABET.lower()
N = len(UK_ALPHABET)



# Криптографічні функції
def caesar_shift_char(ch, k):
    if ch in UK_ALPHABET:
        i = UK_ALPHABET.index(ch)
        return UK_ALPHABET[(i + k) % N]
    if ch in UK_ALPHABET_LOWER:
        i = UK_ALPHABET_LOWER.index(ch)
        return UK_ALPHABET_LOWER[(i + k) % N]
    return ch


def caesar_encrypt(text, k):
    return "".join(caesar_shift_char(ch, k) for ch in text)


def caesar_decrypt(text, k):
    return caesar_encrypt(text, (-k) % N)


def vigenere_encrypt(text, key):
    key_letters = [c for c in key if c.upper() in UK_ALPHABET or c.lower() in UK_ALPHABET_LOWER]
    if not key_letters:
        return text
    out = []
    ki = 0
    for ch in text:
        if ch in UK_ALPHABET or ch in UK_ALPHABET_LOWER:
            k = UK_ALPHABET.index(key_letters[ki % len(key_letters)].upper())
            out.append(caesar_shift_char(ch, k))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def vigenere_decrypt(text, key):
    key_letters = [c for c in key if c.upper() in UK_ALPHABET or c.lower() in UK_ALPHABET_LOWER]
    if not key_letters:
        return text
    out = []
    ki = 0
    for ch in text:
        if ch in UK_ALPHABET or ch in UK_ALPHABET_LOWER:
            k = UK_ALPHABET.index(key_letters[ki % len(key_letters)].upper())
            out.append(caesar_shift_char(ch, (-k) % N))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# Atbash дзеркальна підстановка
ATBASH_MAP = {UK_ALPHABET[i]: UK_ALPHABET[-1 - i] for i in range(N)}
ATBASH_MAP.update({UK_ALPHABET_LOWER[i]: UK_ALPHABET_LOWER[-1 - i] for i in range(N)})


def atbash_transform(text):
    return "".join(ATBASH_MAP.get(ch, ch) for ch in text)



# Допоміжні функції для ключів
def generate_caesar_shift_from_date(date_str):
    digits = [int(c) for c in date_str if c.isdigit()]
    if not digits:
        return 0
    return sum(digits) % N


def generate_vigenere_key_from_surname(surname):
    return surname.replace(" ", "")



# Функції аналізу
def calculate_readability(s):
    """Розрахунок читабельності на основі кількості голосних"""
    vowels = set(list("аеєиіїоуюяАЕЄИІЇОУЮЯ"))
    if not s:
        return 0
    score = sum(1 for ch in s if ch in vowels)
    return (score / len(s)) * 100


def get_key_complexity(alg, key):
    """Оцінка складності ключа"""
    if alg == "caesar":
        return f"Низька (простий числовий зсув: {key})"
    elif alg == "vigenere":
        return f"Середня (ключове слово довжиною {len(key)} символів)"
    else:  # atbash
        return "Низька (фіксоване перетворення без ключа)"



# GUI
class CipherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Порівняльний аналіз шифрів — Caesar, Vigenère, Atbash")
        self.geometry("1000x750")
        self.create_widgets()

    def create_widgets(self):
        # Верхня панель налаштувань
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", padx=8, pady=6)

        ttk.Label(frame_top, text="Введіть текст:").grid(row=0, column=0, sticky="w")

        # Фрейм з текстовим полем та кнопкою вставки
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=8)

        self.input_txt = scrolledtext.ScrolledText(input_frame, wrap="word", height=6)
        self.input_txt.pack(side="left", fill="both", expand=True)
        self.input_txt.insert("1.0", "Захист інформації – важлива дисципліна")

        # Кнопка вставки
        btn_paste = ttk.Button(input_frame, text="Вставити\nз виводу", command=self.paste_from_output, width=12)
        btn_paste.pack(side="right", padx=(4, 0))

        # Алгоритми
        frame_alg = ttk.LabelFrame(self, text="Алгоритм")
        frame_alg.pack(fill="x", padx=8, pady=6)
        self.alg_var = tk.StringVar(value="caesar")
        ttk.Radiobutton(frame_alg, text="Caesar", variable=self.alg_var, value="caesar").pack(side="left", padx=6,
                                                                                              pady=6)
        ttk.Radiobutton(frame_alg, text="Vigenère", variable=self.alg_var, value="vigenere").pack(side="left", padx=6,
                                                                                                  pady=6)
        ttk.Radiobutton(frame_alg, text="Atbash", variable=self.alg_var, value="atbash").pack(side="left", padx=6,
                                                                                              pady=6)

        # Ключі та генерація
        frame_keys = ttk.Frame(self)
        frame_keys.pack(fill="x", padx=8, pady=6)

        ttk.Label(frame_keys, text="Ключ / Параметр:").grid(row=0, column=0, sticky="w")
        self.key_entry = ttk.Entry(frame_keys, width=40)
        self.key_entry.grid(row=0, column=1, sticky="w", padx=6)

        ttk.Button(frame_keys, text="Генерувати з дати", command=self.on_generate_caesar).grid(row=0, column=2, padx=6)
        ttk.Button(frame_keys, text="Генерувати з прізвища", command=self.on_generate_vigenere).grid(row=0, column=3,
                                                                                                     padx=6)
        ttk.Label(frame_keys,
                  text="Для Caesar: числовий зсув. Для Vigenère: текстовий ключ. Для Atbash: ключ не потрібен.").grid(
            row=1, column=1, columnspan=3, sticky="w")

        # Кнопки дій
        frame_actions = ttk.Frame(self)
        frame_actions.pack(fill="x", padx=8, pady=6)
        ttk.Button(frame_actions, text="Зашифрувати", command=self.on_encrypt, width=15).pack(side="left", padx=6)
        ttk.Button(frame_actions, text="Розшифрувати", command=self.on_decrypt, width=15).pack(side="left", padx=6)
        ttk.Button(frame_actions, text="Brute-force (Caesar)", command=self.on_bruteforce, width=18).pack(side="left",
                                                                                                          padx=6)
        ttk.Button(frame_actions, text="Повний аналіз", command=self.on_show_analysis, width=15).pack(side="left",
                                                                                                      padx=6)
        ttk.Button(frame_actions, text="Очистити вихід", command=self.on_clear_output, width=15).pack(side="right",
                                                                                                      padx=6)

        # Вихід
        output_label_frame = ttk.Frame(self)
        output_label_frame.pack(fill="x", padx=8)
        ttk.Label(output_label_frame, text="Результат:").pack(side="left")
        ttk.Button(output_label_frame, text="Копіювати", command=self.copy_output, width=12).pack(side="right")

        self.output_txt = scrolledtext.ScrolledText(self, wrap="word", height=12)
        self.output_txt.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        # Статус
        self.status_var = tk.StringVar(value="Готово до роботи")
        status_label = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_label.pack(fill="x", padx=8, pady=(0, 8))

    # Функції копіювання/вставки
    def copy_output(self):
        """Копіювання виводу в буфер обміну"""
        output = self.output_txt.get("1.0", "end-1c")
        if output:
            self.clipboard_clear()
            self.clipboard_append(output)
            self.status_var.set("Результат скопійовано в буфер обміну")
        else:
            messagebox.showinfo("Копіювання", "Немає тексту для копіювання")

    def paste_from_output(self):
        """Вставка виводу у поле введення"""
        output = self.output_txt.get("1.0", "end-1c")
        if output:
            self.input_txt.delete("1.0", "end")
            self.input_txt.insert("1.0", output)
            self.status_var.set("Вивід вставлено у поле введення")
        else:
            messagebox.showinfo("Вставка", "Немає тексту у виводі для вставки")

    # Обробники кнопок
    def on_generate_caesar(self):
        date = simpledialog.askstring("Дата народження",
                                      "Введіть дату (наприклад 01.01.2000 або 01012000):",
                                      parent=self)
        if date:
            shift = generate_caesar_shift_from_date(date)
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, str(shift))
            self.status_var.set(f"Згенеровано зсув Caesar = {shift} (сума цифр: {date})")

    def on_generate_vigenere(self):
        surname = simpledialog.askstring("Прізвище",
                                         "Введіть прізвище або ключове слово для Vigenère:",
                                         parent=self)
        if surname:
            key = generate_vigenere_key_from_surname(surname)
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key)
            self.status_var.set(f"Згенеровано ключ Vigenère = '{key}'")

    def on_encrypt(self):
        text = self.input_txt.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Помилка", "Введіть текст для шифрування")
            return

        alg = self.alg_var.get()
        key = self.key_entry.get().strip()

        if alg == "caesar":
            if not key:
                messagebox.showerror("Помилка", "Для Caesar введіть числовий зсув у полі ключ")
                return
            try:
                k = int(key)
            except:
                messagebox.showerror("Помилка", "Для Caesar ключ має бути числом")
                return
            res = caesar_encrypt(text, k % N)
            key_info = f"зсув={k % N}"
        elif alg == "vigenere":
            if not key:
                messagebox.showerror("Помилка", "Для Vigenère введіть текстовий ключ (слово)")
                return
            res = vigenere_encrypt(text, key)
            key_info = f"ключ='{key}'"
        else:  # atbash
            res = atbash_transform(text)
            key_info = "без ключа"

        self.output_txt.delete("1.0", "end")
        self.output_txt.insert("1.0", res)
        self.status_var.set(f"Зашифровано ({alg.upper()}, {key_info})")

    def on_decrypt(self):
        text = self.input_txt.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Помилка", "Введіть текст для розшифрування")
            return

        alg = self.alg_var.get()
        key = self.key_entry.get().strip()

        if alg == "caesar":
            if not key:
                messagebox.showerror("Помилка", "Для Caesar введіть числовий зсув у полі ключ")
                return
            try:
                k = int(key)
            except:
                messagebox.showerror("Помилка", "Для Caesar ключ має бути числом")
                return
            res = caesar_decrypt(text, k % N)
            key_info = f"зсув={k % N}"
        elif alg == "vigenere":
            if not key:
                messagebox.showerror("Помилка", "Для Vigenère введіть текстовий ключ (слово)")
                return
            res = vigenere_decrypt(text, key)
            key_info = f"ключ='{key}'"
        else:
            res = atbash_transform(text)
            key_info = "без ключа"

        self.output_txt.delete("1.0", "end")
        self.output_txt.insert("1.0", res)
        self.status_var.set(f"Розшифровано ({alg.upper()}, {key_info})")

    def on_bruteforce(self):
        cipher = self.input_txt.get("1.0", "end-1c")
        if not cipher.strip():
            messagebox.showinfo("Brute-force", "Вставте шифротекст у поле 'Введіть текст' для brute-force")
            return

        results = []
        for shift in range(1, N):
            dec = caesar_decrypt(cipher, shift)
            results.append((shift, dec))

        # Показуємо у новому вікні
        bf_win = tk.Toplevel(self)
        bf_win.title("Brute-force (Caesar) — всі варіанти зсуву")
        bf_win.geometry("900x600")

        ttk.Label(bf_win, text="Всі можливі варіанти розшифрування (перебір усіх зсувів):").pack(pady=6)

        txt = scrolledtext.ScrolledText(bf_win, width=100, height=30, wrap="word")
        txt.pack(fill="both", expand=True, padx=8, pady=8)

        for shift, dec in results:
            txt.insert("end", f"Зсув {shift:2d}: {dec}\n")
        txt.configure(state="disabled")

        ttk.Button(bf_win, text="Закрити", command=bf_win.destroy).pack(pady=6)
        self.status_var.set(f"Brute-force виконано: перевірено {N - 1} варіантів")

    def on_show_analysis(self):
        text = self.input_txt.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showinfo("Аналіз", "Введіть текст для аналізу")
            return

        # Отримуємо ключі
        key = self.key_entry.get().strip()
        try:
            caesar_k = int(key) % N if key else 7
        except:
            caesar_k = 7
        v_key = key if key else "Буман"

        # Шифруємо всіма методами
        caesar_ct = caesar_encrypt(text, caesar_k)
        vigenere_ct = vigenere_encrypt(text, v_key)
        atbash_ct = atbash_transform(text)

        # Обчислюємо метрики
        orig_len = len(text)

        caesar_read = calculate_readability(caesar_ct)
        vigenere_read = calculate_readability(vigenere_ct)
        atbash_read = calculate_readability(atbash_ct)

        # Створюємо вікно аналізу
        a_win = tk.Toplevel(self)
        a_win.title("Повний порівняльний аналіз шифрів")
        a_win.geometry("950x700")

        # Заголовок
        ttk.Label(a_win, text="ПОРІВНЯЛЬНИЙ АНАЛІЗ АЛГОРИТМІВ ШИФРУВАННЯ",
                  font=("Arial", 14, "bold")).pack(pady=10)

        # Таблиця результатів
        table_frame = ttk.LabelFrame(a_win, text="Результати шифрування")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        txt = scrolledtext.ScrolledText(table_frame, wrap="word", height=15, font=("Courier", 10))
        txt.pack(fill="both", expand=True, padx=5, pady=5)

        # Форматована таблиця
        txt.insert("end", f"{'=' * 90}\n")
        txt.insert("end", f"Оригінальний текст ({orig_len} символів):\n")
        txt.insert("end", f"{text}\n")
        txt.insert("end", f"{'=' * 90}\n\n")

        txt.insert("end", f"{'Алгоритм':<15} {'Довжина':<10} {'Читабельність':<15} {'Складність ключа':<30}\n")
        txt.insert("end", f"{'-' * 90}\n")

        txt.insert("end",
                   f"{'Caesar':<15} {len(caesar_ct):<10} {caesar_read:>6.1f}%{'':<7} {get_key_complexity('caesar', caesar_k):<30}\n")
        txt.insert("end", f"Результат: {caesar_ct}\n\n")

        txt.insert("end",
                   f"{'Vigenère':<15} {len(vigenere_ct):<10} {vigenere_read:>6.1f}%{'':<7} {get_key_complexity('vigenere', v_key):<30}\n")
        txt.insert("end", f"Результат: {vigenere_ct}\n\n")

        txt.insert("end",
                   f"{'Atbash':<15} {len(atbash_ct):<10} {atbash_read:>6.1f}%{'':<7} {get_key_complexity('atbash', ''):<30}\n")
        txt.insert("end", f"Результат: {atbash_ct}\n")

        txt.configure(state="disabled")

        # Панель висновків
        conclusion_frame = ttk.LabelFrame(a_win, text="Висновки про стійкість методів")
        conclusion_frame.pack(fill="both", padx=10, pady=5)

        conclusion_txt = scrolledtext.ScrolledText(conclusion_frame, wrap="word", height=10, font=("Arial", 10))
        conclusion_txt.pack(fill="both", expand=True, padx=5, pady=5)

        # Генеруємо висновки
        conclusion = self.generate_conclusions(caesar_k, v_key, caesar_read, vigenere_read, atbash_read)
        conclusion_txt.insert("1.0", conclusion)
        conclusion_txt.configure(state="disabled")

        # Кнопка закриття
        ttk.Button(a_win, text="Закрити", command=a_win.destroy).pack(pady=10)

        self.status_var.set("Показано повний порівняльний аналіз")

    def generate_conclusions(self, caesar_k, v_key, caesar_read, vigenere_read, atbash_read):
        """Генерує текст висновків про стійкість методів"""
        conclusion = "ВИСНОВКИ\n\n"

        conclusion += f"За результатами порівняльного аналізу трьох класичних алгоритмів шифрування можна зробити наступні висновки щодо їх криптографічної стійкості та практичного застосування.\n\n"

        conclusion += f"Шифр Цезаря демонструє найнижчу стійкість серед досліджуваних методів. Використовуючи простий зсув на {caesar_k} позицій в алфавіті, цей метод є вразливим до атаки повного перебору, оскільки існує лише 33 можливих ключі для українського алфавіту. Читабельність зашифрованого тексту становить {caesar_read:.1f}%, що вказує на збереження статистичних властивостей мови. Незважаючи на простоту реалізації, шифр Цезаря не може вважатися надійним для захисту конфіденційної інформації в сучасних умовах.\n\n"

        conclusion += f"Шифр Віженера з ключем '{v_key}' (довжина {len(v_key)} символів) демонструє значно вищу стійкість порівняно з шифром Цезаря. Використання поліалфавітної підстановки ускладнює частотний аналіз та атаки перебору. Читабельність результату складає {vigenere_read:.1f}%, що свідчить про кращу дифузію статистичних властивостей оригінального тексту. Однак стійкість цього методу критично залежить від довжини та непередбачуваності ключа. При використанні короткого або словникового ключа шифр залишається вразливим до криптоаналітичних атак, зокрема методу Касіскі.\n\n"

        conclusion += f"Шифр Атбаш використовує фіксоване зворотне перетворення алфавіту без змінного ключа. Читабельність зашифрованого тексту становить {atbash_read:.1f}%. Головним недоліком цього методу є відсутність секретного ключа, що робить його непридатним для серйозного криптографічного захисту. Атбаш може використовуватися лише як допоміжний метод обфускації або в навчальних цілях.\n\n"

        conclusion += "Загальний висновок: всі три досліджені класичні шифри є застарілими та не відповідають сучасним вимогам інформаційної безпеки. Шифр Віженера демонструє найкращі показники серед розглянутих методів, але навіть він може бути зламаний за допомогою сучасних криптоаналітичних методів. Для надійного захисту інформації необхідно використовувати сучасні криптографічні алгоритми, такі як AES, RSA або еліптичні криві."

        return conclusion

    def on_clear_output(self):
        self.output_txt.delete("1.0", "end")
        self.status_var.set("Вихід очищено")


# ---------------------------
# Запуск програми
# ---------------------------
def main():
    app = CipherGUI()
    app.mainloop()


if __name__ == "__main__":
    main()