"""
Финальный тест всех моделей API.
Проверяет, что все методы работают корректно и модели валидируются без ошибок.
"""

import os
from datetime import date
from dotenv import load_dotenv
from api.client import Account

load_dotenv()


def test_all_endpoints():
    """Тестирует все endpoints API"""
    print("=" * 60)
    print("ТЕСТ ВСЕХ МОДЕЛЕЙ HSE API")
    print("=" * 60)

    # Авторизация
    print("\n[1/6] Авторизация...")
    try:
        account = Account.auth(os.environ['email'], os.environ['password'])
        print("✅ Авторизация успешна")
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        return False

    # Тест get_cafes
    print("\n[2/6] Тестирование get_cafes()...")
    try:
        cafes = account.get_cafes()
        print(f"✅ Получено {len(cafes)} кампусов с кафе")
        total_cafes = sum(len(campus.cafes) for campus in cafes)
        print(f"   Всего кафе: {total_cafes}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

    # Тест get_cafe_info
    print("\n[3/6] Тестирование get_cafe_info()...")
    try:
        cafe_id = "64ed04c9411dc0b2e4890e46"  # Столовая на Покровке
        info = account.get_cafe_info(cafe_id)
        print(f"✅ Получена информация о кафе: {info.cafe_name}")
        print(f"   Адрес: {info.address}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

    # Тест get_cafe_menu
    print("\n[4/6] Тестирование get_cafe_menu()...")
    try:
        cafe_id = "64ed04c9411dc0b2e4890e46"
        menu = account.get_cafe_menu(cafe_id)
        print(f"✅ Получено меню на {menu.current_day}")
        print(f"   Секций в меню: {len(menu.sections)}")
        total_items = sum(len(section.items) for section in menu.sections)
        print(f"   Всего блюд: {total_items}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

    # Тест get_timetable
    print("\n[5/6] Тестирование get_timetable()...")
    try:
        timetable = account.get_timetable()
        print(f"✅ Получено расписание: {len(timetable)} занятий")
        if timetable:
            print(f"   Первое занятие: {timetable[0].discipline}")
            print(f"   Начало: {timetable[0].date_start.strftime('%Y-%m-%d %H:%M')}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

    # Тест get_grades
    print("\n[6/6] Тестирование get_grades()...")
    try:
        grades = account.get_grades()
        print(f"✅ Получены оценки: {len(grades.items)} записей")
        print(f"   Учебный год: {grades.selected_academic_year}")
        print(f"   Программа: {grades.selected_program}")

        # Подсчет оценок с датой
        grades_with_date = sum(1 for item in grades.items if item.date)
        print(f"   Оценок с датой: {grades_with_date}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_all_endpoints()
    exit(0 if success else 1)
