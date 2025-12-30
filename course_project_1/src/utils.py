import collections
import json
import os
from datetime import datetime
from typing import Any, DefaultDict

import pandas as pd  # type: ignore
import requests  # type: ignore
from dotenv import load_dotenv


def xlsx_to_list_of_dict(path: str) -> list[dict[str, object]] | Any:
    """Функция преобразования excel-файла в список словарей.
    На вход подается путь до файла.
    Каждая строка - словарь.
    В каждом словаре ключи - названия столбцов, значения - значения"""
    with open(path, "r", encoding="utf-8"):
        df = pd.read_excel(path)
        return df.to_dict(orient="records")


def xlsx_to_dataframe(path: str) -> pd.DataFrame:
    """Функция открывает указанный Excel-файл и считывает его содержимое
    в структуру pandas DataFrame. Поддерживает стандартные форматы Excel
    и автоматически обрабатывает базовые типы данных."""
    with open(path, "r", encoding="utf-8"):
        df = pd.read_excel(path)
        return df


# Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
# YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными
def greetings() -> str:
    """Приветствие в формате "???",
    где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени."""
    now = (datetime.now()).hour
    if 4 <= now <= 9:
        return "Доброе утро"
    elif 10 <= now <= 16:
        return "Добрый день"
    elif 17 <= now <= 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def operations_in_period(operations: list[dict], date: str) -> list[dict]:
    """Фильтрует операции, совершённые в том же месяце и году, что и указанная дата,
    при условии, что день операции не превышает день указанной даты."""
    input_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    result = []
    for operation in operations:
        data_date = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if input_date.year == data_date.year:
            if input_date.month == data_date.month:
                if input_date.day >= data_date.day:
                    result.append(operation)
    return result


def cards(data: list[dict]) -> list[dict]:
    """Анализирует транзакции по банковским картам и формирует отчёт с суммарными тратами и кэшбэком по каждой карте.

    Для каждой карты (идентифицируемой по номеру) вычисляются:
    - общая сумма трат (по отрицательным значениям «Сумма операции»);
    - накопленный кэшбэк (по положительным значениям «Кэшбэк»).

    Результат возвращается в виде списка словарей с укороченным номером карты (последние 4 цифры)."""
    # Словарь для накопления сумм по каждой карте
    card_totals: DefaultDict[str, dict[str, float]] = collections.defaultdict(
        lambda: {"total_spent": 0.0, "cashback": 0.0}
    )

    # Проходим по всем операциям
    for operation in data:
        card_number = operation["Номер карты"]

        # Накапливаем суммы
        if operation["Сумма операции"] < 0:
            card_totals[card_number]["total_spent"] += operation["Сумма операции"]
        if operation["Кэшбэк"] > 0:
            card_totals[card_number]["cashback"] += operation["Кэшбэк"]

    # Формируем итоговый список словарей
    result = []
    for card_number, totals in card_totals.items():
        result.append(
            {
                "last_digits": str(card_number)[-4:],
                "total_spent": abs(round(totals["total_spent"], 2)),
                "cashback": round(totals["cashback"], 2),
            }
        )

    return result


def top_5_transactions(data: list[dict]) -> list[dict]:
    """Топ-5 транзакций по сумме платежа."""
    sorted_data = sorted(data, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:5]

    result = []
    for operation in sorted_data:
        result.append(
            {
                "date": operation["Дата операции"][:10],
                "amount": abs(round(operation["Сумма операции"], 2)),
                "category": operation["Категория"],
                "description": operation["Описание"],
            }
        )

    return result


def exchange_rate(path: str) -> list[dict]:
    """Курс валют."""
    load_dotenv()
    api_key = os.getenv("API_KEY_APILAYER")
    with open(path, "r", encoding="UTF-8") as f:
        exchanges = json.load(f)["user_currencies"]

    result = []

    for exchange in exchanges:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={exchange}&amount=1"

        payload: dict = {}
        headers = {"apikey": api_key}

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code
        response_text = response.text
        if status_code == 200:
            response_dict = json.loads(response_text)
            result.append(
                {
                    "currency": exchange,
                    "rate": round(response_dict["result"], 2),
                }
            )

    return result


def stock_price(path: str) -> list[dict]:
    """Стоимость акций из S&P500."""
    load_dotenv()
    api_key = os.getenv("API_KEY_ALPHAVANTAGE")
    with open(path, "r", encoding="UTF-8") as f:
        stocks = json.load(f)["user_stocks"]

    result = []

    for stock in stocks:
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()

        if "Time Series (Daily)" in data:
            first_key = next(iter(data["Time Series (Daily)"]))
            price = data["Time Series (Daily)"][first_key]["4. close"]
            result.append({"stock": stock, "price": round(float(price), 2)})

    return result
