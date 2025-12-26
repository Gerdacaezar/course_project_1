from datetime import datetime
from collections import Counter
import pandas as pd


def xlsx_to_list_of_dict(path: str) -> list[dict]:
    """Функция преобразования excel-файла в список словарей.
    На вход подается путь до файла.
    Каждая строка - словарь.
    В каждом словаре ключи - названия столбцов, значения - значения"""
    with open(path, 'r', encoding='utf-8'):
        df = pd.read_excel(path)
        return df.to_dict(orient='records')




# Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
# YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными
def greetings():
    """Приветствие в формате "???",
    где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени."""
    now = (datetime.now()).hour
    if 4 <= now <= 9:
        return 'Доброе утро'
    elif 10 <= now <= 16:
        return 'Добрый день'
    elif 17 <= now <= 22:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def total_amount_of_expenses(data: list[dict]) -> dict:
    """По каждой карте: общая сумма расходов;"""
    result = {}

    for operation in data:
        card_number = operation['Номер карты']
        amount = operation['Сумма операции']

        # Учитываем только расходы (отрицательные суммы)
        if amount < 0:
            if card_number not in result:
                result[card_number] = amount  # Первая операция по карте
            else:
                result[card_number] += amount  # Накопление суммы

    return result


def cashback(data: list[dict]) -> dict:
    """По каждой карте: кэшбек (1 рубль на каждые 100 рублей)."""
    result = {}

    for operation in data:
        card_number = operation['Номер карты']
        amount = operation['Кэшбэк']

        if card_number not in result:
                result[card_number] = amount  # Первая операция по карте
        else:
                result[card_number] += amount  # Накопление суммы

    return result


# print(type(cashback(xlsx_to_list_of_dict('../data/operations.xlsx'))['*5091']))
print(total_amount_of_expenses(xlsx_to_list_of_dict('../data/operations.xlsx')))




def top_5_transactions(data: list[dict]):

    """Топ-5 транзакций по сумме платежа."""
    pass


def exchange_rate():
    """Курс валют."""
    pass


def stock_price():
    """Стоимость акций из S&P500."""
    pass


