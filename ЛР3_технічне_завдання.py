import os
import platform
import subprocess
from PIL import Image

# === Етап 1: Допоміжні функції ===

def text_to_bits(text):
    """Конвертація тексту у двійковий формат (8 біт на символ)"""
    print("[1/5] Конвертація тексту у біти...")
    bits = ''.join(format(ord(c), '08b') for c in text)
    print(f"    Текст: '{text}'")
    print(f"    У бітах: {bits[:64]}{'...' if len(bits) > 64 else ''}")
    return bits

def bits_to_text(bits):
    """Зворотна конвертація двійкових даних у текст"""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    text = ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)
    return text

# === Етап 2: Основна логіка приховування ===

def hide_message(input_path, output_path, message):
    """Приховує повідомлення у PNG-зображенні"""
    print("\n=== ЕТАП ПРИХОВУВАННЯ ===")
    img = Image.open(input_path)
    img = img.convert('RGB')
    pixels = img.load()

    start_marker = "1111111111111110"
    end_marker = "1111111111111111"

    message_bits = start_marker + text_to_bits(message) + end_marker
    print(f"[2/5] Загальна довжина повідомлення: {len(message_bits)} біт")

    width, height = img.size
    max_bits = width * height * 3  # по одному біту в кожен канал R, G, B

    if len(message_bits) > max_bits:
        raise ValueError("Повідомлення занадто довге для цього зображення!")

    print("[3/5] Вбудовування бітів у молодші біти пікселів...")
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index >= len(message_bits):
                break
            r, g, b = pixels[x, y]
            if data_index < len(message_bits):
                r = (r & ~1) | int(message_bits[data_index])
                data_index += 1
            if data_index < len(message_bits):
                g = (g & ~1) | int(message_bits[data_index])
                data_index += 1
            if data_index < len(message_bits):
                b = (b & ~1) | int(message_bits[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
        if data_index >= len(message_bits):
            break

    img.save(output_path, "PNG")
    print(f"[5/5] Повідомлення приховано у '{output_path}'")

    try:
        if platform.system() == "Windows":
            os.startfile(output_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", output_path])
        else:
            subprocess.run(["xdg-open", output_path])
    except Exception:
        print("[!] Не вдалося автоматично відкрити файл.")

def extract_message(image_path):
    """Витягує повідомлення з PNG-зображення"""
    print("\n=== ЕТАП ВИТЯГУВАННЯ ===")
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    bits = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    start_marker = "1111111111111110"
    end_marker = "1111111111111111"

    start = bits.find(start_marker)
    end = bits.find(end_marker, start + len(start_marker))

    if start == -1 or end == -1:
        return "Приховане повідомлення не знайдено."

    message_bits = bits[start + len(start_marker):end]
    message = bits_to_text(message_bits)
    print("[+] Повідомлення успішно витягнуто.")
    return message

def analyze_images(original_path, stego_path):
    """Порівняння оригінального і стеганозображення"""
    print("\n=== АНАЛІЗ ЗМІН ===")
    orig_size = os.path.getsize(original_path)
    stego_size = os.path.getsize(stego_path)
    diff = abs(stego_size - orig_size)

    print(f"Початковий розмір: {orig_size} байт")
    print(f"Новий розмір: {stego_size} байт")
    print(f"Різниця у розмірі: {diff} байт")
    print("Візуальних змін немає, бо змінено лише молодші біти (LSB).")

# === Етап 3: Меню ===

def main():
    while True:
        print("\n==============================")
        print("  С Т Е Г А Н О Г Р А Ф І Я  (PNG)")
        print("==============================")
        print("1. Приховати повідомлення")
        print("2. Витягнути повідомлення")
        print("3. Аналіз змін між зображеннями")
        print("4. Вихід")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            image_path = input("Введіть шлях до PNG-зображення (наприклад, forest.png): ").strip()
            if not os.path.exists(image_path):
                print("[!] Файл не знайдено.")
                continue
            message = input("Введіть повідомлення для приховування: ").strip()
            output_path = "stego_" + os.path.basename(image_path)
            hide_message(image_path, output_path, message)
            analyze_images(image_path, output_path)

        elif choice == "2":
            image_path = input("Введіть шлях до стегозображення (PNG): ").strip()
            if not os.path.exists(image_path):
                print("[!] Файл не знайдено.")
                continue
            extracted = extract_message(image_path)
            print(f"\nВитягнуте повідомлення: {extracted}")

        elif choice == "3":
            orig = input("Оригінальне PNG-зображення: ").strip()
            stego = input("Стегозображення: ").strip()
            if os.path.exists(orig) and os.path.exists(stego):
                analyze_images(orig, stego)
            else:
                print("[!] Один із файлів не знайдено.")

        elif choice == "4":
            print("Вихід із програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
