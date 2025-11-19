import hashlib
import os


def hash_document(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def generate_private_key(name, birthdate, secret):
    data = name + birthdate + secret
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)


def generate_public_key(private_key):
    return (private_key * 7) % 1000007


def sign_document(doc_hash, private_key):
    return int(doc_hash, 16) ^ private_key


def verify_signature(signature_file, doc_file, private_key):
    if not os.path.exists(signature_file):
        print(f"Файл підпису {signature_file} не знайдено!")
        return False
    if not os.path.exists(doc_file):
        print(f"Документ {doc_file} не знайдено!")
        return False

    with open(signature_file, "r") as f:
        signature = int(f.read().strip())

    doc_hash = hash_document(doc_file)
    decrypted = signature ^ private_key
    return decrypted == int(doc_hash, 16)


def create_document(name):
    filename = f"document_{name}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Це тестовий документ користувача {name}.\n")
        f.write("Його буде використано для демонстрації цифрового підпису.")
    return filename


def main():
    global name, private_key, public_key, doc_file, signature_file
    while True:
        print("\n===== МЕНЮ СИСТЕМИ ЦИФРОВОГО ПІДПИСУ =====")
        print("1. Використати тестовий приклад (Петренко)")
        print("2. Створити власні ключі")
        print("3. Створити документ")
        print("4. Підписати документ")
        print("5. Перевірити підпис")
        print("6. Модифікувати документ (перевірка підробки)")
        print("7. Вийти")
        
        choice = input("Оберіть дію (1-7): ")

        if choice == "1":
            print("\n=== Тестовий приклад Петренко ===")
            name = "Petrenko"
            birthdate = "15031995"
            secret = "secret_word"
            private_key = generate_private_key(name, birthdate, secret)
            public_key = generate_public_key(private_key)
            doc_file = create_document(name)
            signature_file = f"signature_{name}.sig"

            print("\nПриватний ключ:", private_key)
            print("Публічний ключ:", public_key)
            print(f"Документ створено: {doc_file}\n")

        elif choice == "2":
            print("\n=== СТВОРЕННЯ КЛЮЧІВ ===")
            name = input("Введіть прізвище: ")
            birthdate = input("Введіть дату народження (наприклад 15031995): ")
            secret = input("Введіть секретне слово: ")

            private_key = generate_private_key(name, birthdate, secret)
            public_key = generate_public_key(private_key)
            signature_file = f"signature_{name}.sig"

            print("\nПриватний ключ:", private_key)
            print("Публічний ключ:", public_key)
            print("Ключі збережено у пам’яті.\n")

        elif choice == "3":
            if "name" not in globals():
                print("Спочатку створіть ключі (пункт 1 або 2).")
                continue

            doc_file = create_document(name)
            print(f"Документ створено: {doc_file}")

        elif choice == "4":
            if "doc_file" not in globals():
                print("Спочатку створіть документ (пункт 3).")
                continue

            doc_hash = hash_document(doc_file)
            signature = sign_document(doc_hash, private_key)

            with open(signature_file, "w") as f:
                f.write(str(signature))

            print("\nДокумент підписано!")
            print("Хеш документа:", doc_hash)
            print("Підпис:", signature)
            print(f"Збережено у файлі {signature_file}\n")

        elif choice == "5":
            doc_to_check = input("Введіть назву документа для перевірки: ")
            sig_to_check = input("Введіть файл підпису: ")

            valid = verify_signature(sig_to_check, doc_to_check, private_key)
            if valid:
                print("\nПідпис ДІЙСНИЙ ✔️")
            else:
                print("\nПідпис ПІДРОБЛЕНИЙ ❌ АБО документ змінено!")

        elif choice == "6":
            if "doc_file" not in globals():
                print("Немає документа.")
                continue

            with open(doc_file, "a", encoding="utf-8") as f:
                f.write("\nНЕСАНКЦІОНОВАНА ЗМІНА!")

            print("\nДокумент змінено! Тепер перевірка повинна провалитися.")

        elif choice == "7":
            print("Вихід...")
            break

        else:
            print("Невірна команда! Спробуйте знову.")


if __name__ == "__main__":
    main()
