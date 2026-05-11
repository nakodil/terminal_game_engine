import sys

def test_ansi_sequences():
    # Базовые стили оформления
    styles = {
        "Обычный": "0",
        "Жирный": "1",
        "Тонкий (Dim)": "2",
        "Курсив": "3",
        "Подчеркнутый": "4",
        "Мигающий": "5",
        "Инверсия": "7",
        "Скрытый": "8",
        "Зачеркнутый": "9"
    }

    # Стандартные цвета (30-37 — текст, 40-47 — фон)
    colors = {
        "Черный": "0",
        "Красный": "1",
        "Зеленый": "2",
        "Желтый": "3",
        "Синий": "4",
        "Пурпурный": "5",
        "Циан": "6",
        "Белый": "7"
    }

    print("\n--- ТЕСТИРОВАНИЕ СТИЛЕЙ ТЕКСТА ---")
    for name, code in styles.items():
        print(f"\033[{code}m{name} (код {code})\033[0m", end="  ")
    print("\n")

    print("--- ТЕСТИРОВАНИЕ ЦВЕТОВ ТЕКСТА ---")
    # Стандартные (3x) и яркие (9x)
    for name, code in colors.items():
        standard = f"\033[3{code}m{name}\033[0m"
        bright = f"\033[9{code}mЯркий {name}\033[0m"
        print(f"{standard:<20} {bright}")
    print()

    print("--- ТЕСТИРОВАНИЕ ФОНОВЫХ ЦВЕТОВ ---")
    for name, code in colors.items():
        # Фон (4x) и текст (3x) для контраста
        bg_standard = f"\033[4{code};37m {name} \033[0m"
        bg_bright = f"\033[10{code};30m Яркий {name} \033[0m"
        print(f"{bg_standard} {bg_bright}")
    print()

    print("--- КОМБИНИРОВАННЫЙ ТЕСТ ---")
    print("\033[1;31;43m ЖИРНЫЙ КРАСНЫЙ НА ЖЕЛТОМ \033[0m")
    print("\033[4;94;107m ПОДЧЕРКНУТЫЙ СИНИЙ НА БЕЛОМ \033[0m")
    print("\nТест завершен!")

if __name__ == "__main__":
    # Проверка: некоторые терминалы Windows требуют инициализации

    if sys.platform == "win32":
            import os
            os.system('color')
    test_ansi_sequences()