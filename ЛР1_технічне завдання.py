import time
import re

def loading_effect():
    print("\n🔍 Виконується аналіз паролю", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(1)
    print("\n")

def analyze_password(password, name, birthdate):
    score = 0
    recommendations = []

    # 1. Аналіз довжини
    length = len(password)
    if length >= 16:
        score += 5
    elif length >= 12:
        score += 4
    elif length >= 8:
        score += 3
    elif length >= 6:
        score += 1
    else:
        recommendations.append("Пароль занадто короткий — мінімум 8 символів.")

    # 2. Підрахунок символів
    lower_count = sum(1 for c in password if c.islower())
    upper_count = sum(1 for c in password if c.isupper())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(1 for c in password if not c.isalnum())

    has_lower = lower_count > 0
    has_upper = upper_count > 0
    has_digit = digit_count > 0
    has_special = special_count > 0

    variety_score = sum([has_lower, has_upper, has_digit, has_special])
    score += variety_score

    # 3. Аналіз персональних даних
    personal_risk = False
    name_lower = name.lower()
    birth_year_match = re.findall(r"\d{4}", birthdate)
    birth_year = birth_year_match[0] if birth_year_match else ""
    birth_digits = re.sub(r"\D", "", birthdate)

    lowered_pass = password.lower()

    if name_lower and name_lower in lowered_pass:
        personal_risk = True
        score -= 4
        recommendations.append("Пароль містить ваше ім’я — це критично небезпечно.")
    if birth_year and birth_year in lowered_pass:
        personal_risk = True
        score -= 3
        recommendations.append("Пароль містить ваш рік народження — легко вгадати.")
    if birth_digits and birth_digits in lowered_pass:
        personal_risk = True
        score -= 3
        recommendations.append("Пароль містить вашу дату народження — не рекомендується.")

    # 4. Перевірка словникових слів
    common_words = ["password", "qwerty", "admin", "user", "login", "test", "abc", "1234"]
    if any(word in lowered_pass for word in common_words):
        score -= 2
        recommendations.append("Пароль містить популярне слово або послідовність символів — це робить його вразливим.")



    # 6. Рівень безпеки
    if score <= 2:
        level = "😓 Дуже слабкий"
    elif score <= 4:
        level = "🥲 Слабкий"
    elif score <= 5:
        level = "🫤 Середній"
    elif score <= 7:
        level = "🙂 Надійний"
    else:
        level = "🤩 Дуже надійний"

    # Статистика
    print("РЕЗУЛЬТАТ АНАЛІЗУ ПАРОЛЮ")
    print(f"Довжина паролю: {length} символів")
    print(f"🔤 Малі літери: {'✅' if has_lower else '⛔'} ({lower_count})")
    print(f"🅰️ Великі літери: {'✅' if has_upper else '⛔'} ({upper_count})")
    print(f"🔢 Цифри: {'✅' if has_digit else '⛔'} ({digit_count})")
    print(f"🔣 Спецсимволи: {'✅' if has_special else '⛔'} ({special_count})")
    print(f"👤 Персональні дані у паролі: {'⚠️ Так' if personal_risk else '✅ Ні'}")
    print(f"📊 Оцінка складності: {score}/10 — {level}\n")

    #Рекомендації
    print("💡 РЕКОМЕНДАЦІЇ:")
    if not has_upper:
        recommendations.append("Додайте хоча б одну велику літеру — це підвищить стійкість.")
    if not has_digit:
        recommendations.append("Додайте хоча б одну цифру для підвищення складності.")
    if not has_special:
        recommendations.append("Додайте спеціальні символи (!, @, #, $, %, тощо).")
    if len(password) < 12:
        recommendations.append("Збільште довжину паролю хоча б до 12 символів.")
    if len(recommendations) == 0:
        recommendations.append("Ваш пароль чудовий — відповідає усім вимогам безпеки!")


    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

    # 🔸 9. Підсумок
    if score < 6:
        print("\n⚠️ Рекомендується змінити пароль якнайшвидше!")
    else:
        print("\n✅ Пароль має прийнятний рівень безпеки.")

def main():
    while True:
        print("\nМЕНЮ ПРОГРАМИ АНАЛІЗУ ПАРОЛЮ")
        print("1. Перевірити пароль")
        print("2. Вийти з програми")

        choice = input("👉 Оберіть дію (1/2): ").strip()
        if choice == "1":
            name = input("\nВведіть ваше ім’я: ").strip()
            birthdate = input("Введіть дату народження (у форматі дд.мм.рррр): ").strip()
            password = input("Введіть пароль для перевірки: ").strip()

            loading_effect()
            analyze_password(password, name, birthdate)

        elif choice == "2":
            print("\n👋 Програму завершено. Дякуємо за використання!")
            break
        else:
            print("⚠️ Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main()
