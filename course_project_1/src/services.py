import json
from datetime import datetime


# Напишите функцию для анализа выгодности категорий повышенного кэшбека.
def cashback_categories(data: list[dict], year: str | int, month: str | int) -> str:
    """На вход функции поступают данные для анализа, год и месяц.
    Входные параметры:
    data — данные с транзакциями;
    year — год, за который проводится анализ;
    month — месяц, за который проводится анализ.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать кэшбека в указанном месяце года.

    Выходные параметры
    JSON с анализом, сколько на каждой категории можно заработать кэшбека.
    Формат выходных данных:
    {"Категория 1": 1000, "Категория 2": 2000, "Категория 3": 500}"""
    card_totals = {}

    # Проходим по всем операциям
    for operation in data:
        date = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if date.year == int(year) and date.month == int(month):
            category = operation["Категория"]

            # Накапливаем суммы
            if operation["Сумма операции"] < 0 and operation["Категория"] != "Переводы":
                if category not in card_totals:
                    card_totals[category] = operation["Сумма операции"]
                else:
                    card_totals[category] += operation["Сумма операции"]

    for category in card_totals:
        card_totals[category] = abs(round(card_totals[category]) // 100)
    sorted_categories = dict(sorted(card_totals.items(), key=lambda item: item[1], reverse=True))

    return json.dumps(sorted_categories, indent=4, ensure_ascii=False)
