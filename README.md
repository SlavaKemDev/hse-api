# HSE API

Python библиотека для работы с API мобильного приложения [HSE App X](https://apps.apple.com/us/app/hse-app-x/id1527320487).

## Описание

Библиотека предоставляет удобный Python-интерфейс для взаимодействия с API HSE App X. Позволяет получать информацию о:
- Расписании занятий
- Оценках и успеваемости
- Столовых и меню кампусов ВШЭ

Все модели данных реализованы с использованием Pydantic для валидации и типобезопасности.

## Установка

### Клонирование репозитория

```bash
git clone https://github.com/SlavaKemDev/hse-api.git
cd hse-api
```

### Установка зависимостей

Установите все необходимые зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Либо с использованием pip3:

```bash
pip3 install -r requirements.txt
```

## Быстрый старт

### 1. Настройка окружения

Создайте файл `.env` в корне проекта и добавьте свои учетные данные:

```env
email=ваш_email@edu.hse.ru
password=ваш_пароль
```

### 2. Авторизация

```python
from api.client import Account
from dotenv import load_dotenv
import os

load_dotenv()

# Авторизация через email и пароль
account = Account.auth(os.environ['email'], os.environ['password'])
```

### 3. Использование API

```python
from datetime import date

# Получить расписание на сегодня
timetable = account.get_timetable()
for lesson in timetable:
    print(f"{lesson.discipline} - {lesson.auditorium}")

# Получить оценки
grades = account.get_grades()
print(f"Всего оценок: {len(grades.items)}")

# Получить список столовых
cafes = account.get_cafes()
for campus in cafes:
    print(f"{campus.campus_name}: {len(campus.cafes)} кафе")

# Получить меню конкретной столовой
cafe_id = "64ed04c9411dc0b2e4890e46"  # Столовая на Покровке
menu = account.get_cafe_menu(cafe_id)
print(f"Меню на {menu.current_day}")
for section in menu.sections:
    print(f"\n{section.section_name}:")
    for item in section.items:
        print(f"  - {item.item_name}: {item.price}₽")
```

## API Reference

### Класс `Account`

Основной класс для работы с API.

#### Методы авторизации

##### `Account.auth(email: str, password: str) -> Account`
Создает экземпляр аккаунта через авторизацию по email и паролю.

**Параметры:**
- `email` - корпоративная почта НИУ ВШЭ
- `password` - пароль от аккаунта

**Возвращает:** объект `Account`

**Исключения:**
- `AuthError` - неверные учетные данные
- `NetworkError` - проблемы с сетью

#### Методы API

##### `get_timetable(email: Optional[str] = None, start_date: Optional[date] = None)`
Получает расписание занятий.

**Параметры:**
- `email` - email студента (по умолчанию используется email текущего аккаунта)
- `start_date` - дата начала периода (по умолчанию сегодня)

**Возвращает:** список объектов `Lesson`

**Пример:**
```python
from datetime import date

# Расписание на сегодня
lessons = account.get_timetable()

# Расписание на конкретную дату
lessons = account.get_timetable(start_date=date(2025, 11, 15))
```

##### `get_grades(academic_year: Optional[str] = None, program_id: Optional[int] = None)`
Получает информацию об оценках.

**Параметры:**
- `academic_year` - учебный год (например, "2024-2025")
- `program_id` - ID образовательной программы

**Возвращает:** объект `GradesResponse`

**Пример:**
```python
# Оценки за текущий год
grades = account.get_grades()

# Оценки за конкретный учебный год
grades = account.get_grades(academic_year="2024-2025")

# Доступные учебные годы
print(grades.available_academic_years)

# Перебор всех оценок
for item in grades.items:
    if item.grade:
        print(f"{item.discipline}: {item.grade.ten_point_scale}")
```

##### `get_cafes()`
Получает список всех столовых по кампусам.

**Возвращает:** список объектов `CampusCafes`

**Пример:**
```python
cafes = account.get_cafes()
for campus in cafes:
    print(f"\n{campus.campus_name}:")
    for cafe in campus.cafes:
        print(f"  - {cafe.cafe_name}")
        print(f"    Адрес: {cafe.address}")
        print(f"    Есть меню: {'Да' if cafe.has_menu else 'Нет'}")
```

##### `get_cafe_info(cafe_id: str)`
Получает детальную информацию о конкретной столовой.

**Параметры:**
- `cafe_id` - ID столовой

**Возвращает:** объект `CafeInfo`

**Пример:**
```python
cafe_id = "64ed04c9411dc0b2e4890e46"
info = account.get_cafe_info(cafe_id)
print(f"Название: {info.cafe_name}")
print(f"Адрес: {info.address}")
print(f"Координаты: {info.coordinates.lat}, {info.coordinates.lng}")

# Время работы
for hours in info.opening_hours:
    if hours.is_open:
        print(f"{hours.day_of_week}: {hours.start_time} - {hours.end_time}")
```

##### `get_cafe_menu(cafe_id: str)`
Получает меню столовой на текущий день.

**Параметры:**
- `cafe_id` - ID столовой

**Возвращает:** объект `CafeMenu`

**Пример:**
```python
cafe_id = "64ed04c9411dc0b2e4890e46"
menu = account.get_cafe_menu(cafe_id)

print(f"Меню на {menu.current_day}")
print(f"Доступные дни: {', '.join(menu.available_days)}")

for section in menu.sections:
    print(f"\n{section.section_name}:")
    for item in section.items:
        price = f"{item.price}₽" if item.price else "Цена не указана"
        print(f"  - {item.item_name}: {price}")
        if item.composition:
            print(f"    Состав: {item.composition}")
```

## Модели данных

### Расписание

#### `Lesson`
Представляет одно занятие в расписании.

**Основные поля:**
- `discipline: str` - название дисциплины
- `type: str` - тип занятия (Лекция, Семинар и т.д.)
- `auditorium: str` - аудитория
- `building: str` - корпус
- `date_start: datetime` - время начала
- `date_end: datetime` - время окончания
- `lecturer_profiles: List[LecturerProfile]` - список преподавателей
- `stream_links: List[StreamLink]` - ссылки на онлайн-трансляции (если есть)
- `note: str` - заметки к занятию

#### `LecturerProfile`
Информация о преподавателе.

**Поля:**
- `full_name: str` - ФИО
- `email: str` - email
- `avatar_url: str` - URL аватара
- `description: str` - описание/должность

### Оценки

#### `GradesResponse`
Ответ API с оценками.

**Поля:**
- `items: List[GradeItem]` - список оценок
- `available_academic_years: List[str]` - доступные учебные годы
- `selected_academic_year: str` - выбранный учебный год
- `available_programs: List[ProgramInfo]` - доступные программы обучения
- `current_academic_year: str` - текущий учебный год

#### `GradeItem`
Одна оценка.

**Поля:**
- `discipline: str` - название дисциплины
- `grade: GradeValue` - оценка (содержит `ten_point_scale`, `five_point_scale`, `pass_`)
- `date: date` - дата получения оценки
- `type_raw: str` - тип контроля (Экзамен, Зачет и т.д.)
- `module_num: str` - номер модуля
- `credits: int` - количество кредитов
- `lecturer: str` - преподаватель

### Столовые

#### `CampusCafes`
Столовые одного кампуса.

**Поля:**
- `campus_name: str` - название кампуса
- `campus_id: str` - ID кампуса
- `cafes: List[Cafe]` - список столовых
- `coordinates: Coordinates` - координаты кампуса

#### `Cafe`
Информация о столовой.

**Поля:**
- `cafe_id: str` - ID столовой
- `cafe_name: str` - название
- `address: str` - адрес
- `coordinates: Coordinates` - координаты (lat, lng)
- `has_menu: bool` - доступно ли меню
- `opening_hours: List[OpeningHours]` - время работы по дням недели
- `photos: List[str]` - фотографии
- `navigation: Navigation` - навигация (этаж, кабинет)

#### `CafeMenu`
Меню столовой.

**Поля:**
- `cafe_id: str` - ID столовой
- `current_day: str` - текущий день
- `available_days: List[str]` - доступные дни
- `sections: List[MenuSection]` - секции меню

#### `MenuSection`
Секция меню (например, "Салаты", "Горячее" и т.д.).

**Поля:**
- `section_name: str` - название секции
- `items: List[MenuItem]` - список блюд
- `price: int` - цена (для комплексных обедов)

#### `MenuItem`
Блюдо в меню.

**Поля:**
- `item_name: str` - название блюда
- `item_id: str` - ID блюда
- `price: int` - цена в рублях
- `composition: str` - состав
- `section: str` - секция
- `props: List[MenuProp]` - свойства (калории, белки, жиры, углеводы)
- `chips: List[str]` - теги (например, "Вегетарианское")

## Примеры использования

### Пример 1: Вывод расписания на сегодня

```python
import os
from dotenv import load_dotenv
from api.client import Account

load_dotenv()

account = Account.auth(os.environ['email'], os.environ['password'])
lessons = account.get_timetable()

print("Расписание на сегодня:\n")
for lesson in lessons:
    print(f"⏰ {lesson.date_start.strftime('%H:%M')} - {lesson.date_end.strftime('%H:%M')}")
    print(f"📚 {lesson.discipline}")
    print(f"📍 {lesson.building}, ауд. {lesson.auditorium}")
    print(f"👨‍🏫 {', '.join(p.full_name for p in lesson.lecturer_profiles)}")
    print()
```

### Пример 2: Получение меню столовой

```python
import json
import os
from dotenv import load_dotenv
from api.client import Account

load_dotenv()

account = Account.auth(os.environ['email'], os.environ['password'])
cafe_id = "64ed04c9411dc0b2e4890e46"  # Столовая на Покровке

menu = account.get_cafe_menu(cafe_id)

# Сохранение в JSON
with open("today_menu.json", "w", encoding="utf-8") as f:
    json.dump(menu.model_dump(), f, ensure_ascii=False, indent=4, default=str)

print(f"Меню на {menu.current_day} сохранено в today_menu.json")
```

### Пример 3: Анализ успеваемости

```python
import os
from dotenv import load_dotenv
from api.client import Account

load_dotenv()

account = Account.auth(os.environ['email'], os.environ['password'])
grades = account.get_grades()

# Статистика по оценкам
grades_with_marks = [g for g in grades.items if g.grade]

if grades_with_marks:
    avg = sum(g.grade.ten_point_scale for g in grades_with_marks) / len(grades_with_marks)
    print(f"Средний балл: {avg:.2f}")
    
    # Распределение оценок
    distribution = {}
    for g in grades_with_marks:
        mark = g.grade.ten_point_scale
        distribution[mark] = distribution.get(mark, 0) + 1
    
    print("\nРаспределение оценок:")
    for mark in sorted(distribution.keys(), reverse=True):
        print(f"  {mark}: {'█' * distribution[mark]} ({distribution[mark]})")
```

### Пример 4: Полный тест всех API

Запустите встроенный тестовый скрипт:

```bash
python test_all_models.py
```

Этот скрипт проверит работу всех endpoints и выведет подробную информацию о каждом запросе.

## Обработка ошибок

Библиотека использует кастомные исключения для обработки ошибок:

```python
from api.client import Account
from api.exceptions import AuthError, NetworkError

try:
    account = Account.auth("email@edu.hse.ru", "password")
    lessons = account.get_timetable()
except AuthError as e:
    print(f"Ошибка авторизации: {e}")
except NetworkError as e:
    print(f"Ошибка сети: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
```

## Структура проекта

```
hse-api/
├── api/
│   ├── __init__.py
│   ├── auth.py           # Авторизация через OIDC
│   ├── client.py         # Основной класс Account
│   ├── config.py         # Конфигурация URL API
│   ├── exceptions.py     # Кастомные исключения
│   ├── http.py           # HTTP клиент с поддержкой refresh token
│   ├── endpoints/        # API endpoints
│   │   ├── food.py       # Методы для работы со столовыми
│   │   ├── grades.py     # Методы для работы с оценками
│   │   └── ruz.py        # Методы для работы с расписанием
│   └── models/           # Pydantic модели
│       ├── cafes.py      # Модели столовых и меню
│       ├── grades.py     # Модели оценок
│       └── timetable.py  # Модели расписания
├── get_today_menu.py     # Пример получения меню
├── test_all_models.py    # Тест всех API
├── requirements.txt      # Зависимости проекта
└── README.md             # Документация
```

## Технические детали

### Авторизация

Библиотека использует OAuth 2.0 (OIDC) для авторизации через `password grant` flow. После успешной авторизации:
- Access token используется для API запросов
- Refresh token автоматически обновляет access token при истечении срока действия

### HTTP клиент

Встроенный HTTP клиент (`HttpClient`) автоматически:
- Добавляет Authorization header к каждому запросу
- Обновляет токен при получении 401 ошибки
- Обрабатывает типовые ошибки API

### Валидация данных

Все ответы API валидируются через Pydantic модели, что обеспечивает:
- Типобезопасность
- Автоматическую конвертацию типов
- Проверку обязательных полей
- Удобный доступ к данным через атрибуты

## Ограничения

- API может измениться без предупреждения
- Требуется валидный аккаунт НИУ ВШЭ для доступа

## Лицензия

См. файл [LICENSE](LICENSE)

## Контакты

Если у вас есть вопросы или предложения, создайте issue в репозитории.

