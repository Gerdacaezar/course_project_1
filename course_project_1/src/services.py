import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# Напишите функцию для анализа выгодности категорий повышенного кэшбека.
def cashback_categories(data: list[dict], year: str | int, month: str | int) -> str:
    """
    Анализирует транзакции за указанный месяц и год, рассчитывает суммы трат по категориям
    (исключая переводы) и формирует JSON‑строку с категориями, отсортированными по убыванию трат.

    Параметры:
        data (list[dict]): список словарей с данными о транзакциях. Каждый словарь должен содержать:
            - "Дата операции" (str): дата и время операции в формате "дд.мм.гггг ЧЧ:ММ:СС";
            - "Категория" (str): категория транзакции;
            - "Сумма операции" (float/int): сумма операции (отрицательные значения — расходы).
        year (str | int): год для фильтрации транзакций (может быть строкой или числом).
        month (str | int): месяц для фильтрации транзакций (может быть строкой или числом).

    Возвращаемое значение:
        str: JSON‑строка с отсортированным по убыванию сумм словарем, где:
            - ключи — названия категорий;
            - значения — суммы трат в сотнях рублей (округлённые вниз, без знака минус).
        Пример:
        {
            "Продукты": 150,
            "Развлечения": 75,
            "Одежда": 40
        }
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции home_page")

    try:
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

        logger.info("Вывод результатов работы функции cashback_categories")
        return json.dumps(sorted_categories, indent=4, ensure_ascii=False)

    except Exception as E:
        logger.error(f"Ошибка {E} в функции cashback_categories")
        return ""
