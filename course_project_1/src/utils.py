import collections
import json
import logging
import os
from datetime import datetime
from typing import Any, DefaultDict, Optional

import pandas as pd  # type: ignore
import requests  # type: ignore
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def xlsx_to_list_of_dict(path: str) -> list[dict[str, object]] | Any:
    """
        Преобразует Excel‑файл (xlsx) в список словарей, где каждый словарь соответствует строке таблицы.

    Параметры:
        path (str): абсолютный или относительный путь к xlsx‑файлу.

    Возвращаемое значение:
        list[dict[str, object]]: список словарей. Каждый словарь представляет одну строку таблицы:
            - ключи — названия столбцов из Excel (как строки);
            - значения — соответствующие данные из ячеек (тип сохраняется как в Excel).
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции xlsx_to_list_of_dict")

    try:
        with open(path, "r", encoding="utf-8"):
            df = pd.read_excel(path)

            logger.info("Вывод результатов работы функции xlsx_to_list_of_dict")
            return df.to_dict(orient="records")
    except Exception as E:
        logger.error(f"Ошибка {E} в функции xlsx_to_list_of_dict")
        return []


def xlsx_to_dataframe(path: str) -> pd.DataFrame | str:
    """
        Считывает Excel‑файл (xlsx) и возвращает его содержимое в виде объекта pandas.DataFrame.

    Параметры:
        path (str): путь к xlsx‑файлу (абсолютный или относительный).

    Возвращаемое значение:
        pd.DataFrame: DataFrame, содержащий данные из Excel‑файла.
            - Индексы строк соответствуют номерам строк в Excel (начиная с 0).
            - Названия столбцов сохраняются как в исходном файле (тип — str).
            - Типы данных столбцов определяются автоматически pandas (int, float, str, datetime и др.).
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции xlsx_to_dataframe")

    try:
        with open(path, "r", encoding="utf-8"):
            df = pd.read_excel(path)

            logger.info("Вывод результатов работы функции xlsx_to_dataframe")
            return df

    except Exception as E:
        logger.error(f"Ошибка {E} в функции xlsx_to_dataframe")
        return ""


# Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
# YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными
def greetings(now: Optional[Any] = None) -> str:
    """
        Возвращает приветственное сообщение в зависимости от времени суток.

    Параметры:
        now (Any, optional): момент времени для определения приветствия.
            Может быть объектом datetime, timestamp или None.
            Если None — используется текущее локальное время.

    Возвращаемое значение:
        str: приветствие на русском языке:
            - "Доброе утро" — с 4:00 до 9:59;
            - "Добрый день" — с 10:00 до 16:59;
            - "Добрый вечер" — с 17:00 до 22:59;
            - "Доброй ночи" — с 23:00 до 3:59.
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции greetings")

    try:
        if now is None:
            now = datetime.now()
        hour = now.hour
        if 4 <= hour <= 9:
            message = "Доброе утро"
        elif 10 <= hour <= 16:
            message = "Добрый день"
        elif 17 <= hour <= 22:
            message = "Добрый вечер"
        else:
            message = "Доброй ночи"

        logger.info("Вывод результатов работы функции greetings")
        return message

    except Exception as E:
        logger.error(f"Ошибка {E} в функции greetings")
        return ""


def operations_in_period(operations: list[dict], date: str) -> list[dict]:
    """
    Фильтрует список операций, оставляя только те, что произошли в том же месяце и году,
    что и указанная дата, при этом дата операции не позже указанной даты.

    Параметры:
        operations (list[dict]): список словарей, представляющих финансовые операции.
            Каждый словарь должен содержать ключ "Дата операции" со значением в формате
            "дд.мм.ГГГГ ЧЧ:ММ:СС" (например, "15.01.2025 10:30:00").
        date (str): строка с датой и временем в формате "ГГГГ‑мм‑дд ЧЧ:ММ:СС"
            (например, "2025‑01‑31 23:59:59"), относительно которой выполняется фильтрация.

    Возвращаемое значение:
        list[dict]: отфильтрованный список операций (словарей), удовлетворяющих условиям:
            - год операции совпадает с годом указанной даты;
            - месяц операции совпадает с месяцем указанной даты;
            - день операции не превышает день указанной даты.
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции operations_in_period")

    try:
        input_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        result = []
        for operation in operations:
            data_date = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if input_date.year == data_date.year:
                if input_date.month == data_date.month:
                    if input_date.day >= data_date.day:
                        result.append(operation)

        logger.info("Вывод результатов работы функции operations_in_period")
        return result

    except Exception as E:
        logger.error(f"Ошибка {E} в функции operations_in_period")
        return []


def cards(data: list[dict]) -> list[dict]:
    """
    Анализирует транзакции по банковским картам и формирует сводную статистику по каждой карте.

    Параметры:
        data (list[dict]): список словарей с данными о транзакциях. Каждый словарь должен содержать:
            - "Номер карты" (str/int): полный номер карты;
            - "Сумма операции" (float/int): сумма транзакции (отрицательные значения — расходы);
            - "Кэшбэк" (float/int): начисленный кэшбэк (положительные значения).

    Возвращаемое значение:
        list[dict]: список словарей со статистикой по каждой карте. Каждый словарь содержит:
            - "last_digits" (str): последние 4 цифры номера карты;
            - "total_spent" (float): общая сумма расходов (по модулю, округлено до 2 знаков);
            - "cashback" (float): общая сумма начисленного кэшбека (округлено до 2 знаков).
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции cards")

    try:
        card_totals: DefaultDict[str, dict[str, float]] = collections.defaultdict(
            lambda: {"total_spent": 0.0, "cashback": 0.0}
        )

        for operation in data:
            card_number = operation["Номер карты"]

            if operation["Сумма операции"] < 0:
                card_totals[card_number]["total_spent"] += operation["Сумма операции"]
            if operation["Кэшбэк"] > 0:
                card_totals[card_number]["cashback"] += operation["Кэшбэк"]

        result = []
        for card_number, totals in card_totals.items():
            result.append(
                {
                    "last_digits": str(card_number)[-4:],
                    "total_spent": abs(round(totals["total_spent"], 2)),
                    "cashback": round(totals["cashback"], 2),
                }
            )

        logger.info("Вывод результатов работы функции cards")
        return result

    except Exception as E:
        logger.error(f"Ошибка {E} в функции cards")
        return []


def top_5_transactions(data: list[dict]) -> list[dict]:
    """
    Возвращает топ‑5 транзакций с наибольшими по модулю суммами операций.

    Параметры:
        data (list[dict]): список словарей с данными о транзакциях. Каждый словарь должен содержать:
            - "Сумма операции" (float/int): сумма транзакции (знак указывает на тип операции);
            - "Дата операции" (str): дата и время операции в формате "ДД.ММ.ГГГГ ЧЧ:ММ:СС";
            - "Категория" (str): категория транзакции;
            - "Описание" (str): описание транзакции.

    Возвращаемое значение:
        list[dict]: список из не более чем 5 словарей (по числу топ‑транзакций).
        Каждый словарь содержит:
            - "date" (str): дата операции в формате "ГГГГ‑ММ‑ДД" (первые 10 символов исходной строки);
            - "amount" (float): сумма операции по модулю, округлённая до 2 знаков после запятой;
            - "category" (str): категория транзакции;
            - "description" (str): описание транзакции.
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции top_5_transactions")

    try:
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

        logger.info("Вывод результатов работы функции top_5_transactions")
        return result

    except Exception as E:
        logger.error(f"Ошибка {E} в функции top_5_transactions")
        return []


def exchange_rate(path: str) -> list[dict]:
    """
    Получает текущие курсы обмена указанных валют к рублю (RUB) через API Apilayer.

    Параметры:
        path (str): путь к JSON‑файлу, содержащему список валют для конвертации.
            Файл должен иметь ключ "user_currencies", значением которого является
            список строк (кодов валют, например: ["USD", "EUR", "CNY"]).

    Возвращаемое значение:
        list[dict]: список словарей с курсами валют. Каждый словарь содержит:
            - "currency" (str): код запрашиваемой валюты (например, "USD");
            - "rate" (float): курс обмена 1 единицы валюты к RUB, округлённый до 2 знаков после запятой.
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции exchange_rate")

    try:
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
                try:
                    response_dict = json.loads(response_text)
                    if "result" in response_dict:
                        result.append(
                            {
                                "currency": exchange,
                                "rate": round(response_dict["result"], 2),
                            }
                        )
                except json.JSONDecodeError:
                    continue

        logger.info("Вывод результатов работы функции exchange_rate")
        return result

    except Exception as E:
        logger.error(f"Ошибка {E} в функции exchange_rate")
        return []


def stock_price(path: str) -> list[dict]:
    """
    Получает текущие цены акций из списка компаний через API Alpha Vantage.

    Параметры:
        path (str): путь к JSON‑файлу, содержащему список тикеров акций для запроса.
            Файл должен иметь ключ "user_stocks", значением которого является
            список строк (тикеров, например: ["AAPL", "GOOGL", "TSLA"]).

    Возвращаемое значение:
        list[dict]: список словарей с текущими ценами акций. Каждый словарь содержит:
            - "stock" (str): тикер акции (например, "AAPL");
            - "price" (float): текущая цена закрытия (поле "4. close") из последнего
              доступного дня в таймсерии, округлённая до 2 знаков после запятой.
        При возникновении ошибки возвращает пустой список [].
    """
    logger.info("Запуск функции stock_price")

    try:
        load_dotenv()
        api_key = os.getenv("API_KEY_ALPHAVANTAGE")
        with open(path, "r", encoding="UTF-8") as f:
            stocks = json.load(f)["user_stocks"]

        result = []

        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={api_key}"
            r = requests.get(url)
            data = r.json()

            if "Time Series (Daily)" in data:
                first_key = next(iter(data["Time Series (Daily)"]))
                price = data["Time Series (Daily)"][first_key]["4. close"]
                result.append({"stock": stock, "price": round(float(price), 2)})

        logger.info("Вывод результатов работы функции stock_price")
        return result

    except Exception as E:
        logger.error(f"Ошибка {E} в функции stock_price")
        return []
