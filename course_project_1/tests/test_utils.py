import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (cards, exchange_rate, greetings, operations_in_period, stock_price, top_5_transactions,
                       xlsx_to_dataframe, xlsx_to_list_of_dict)


@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_xlsx_to_list_of_dict(mock_read_excel, mock_file, list_operations):
    mock_read_excel.return_value = pd.DataFrame(list_operations)
    result = xlsx_to_list_of_dict("example.xlsx")
    mock_file.assert_called_once_with("example.xlsx", "r", encoding="utf-8")
    mock_read_excel.assert_called_once()
    expected = list_operations
    assert expected == result


@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_xlsx_to_dataframe(mock_read_excel, mock_file, list_operations):
    mock_read_excel.return_value = pd.DataFrame(list_operations)
    result = xlsx_to_dataframe("example.xlsx")
    mock_file.assert_called_once_with("example.xlsx", "r", encoding="utf-8")
    mock_read_excel.assert_called_once()
    expected = pd.DataFrame(list_operations)
    assert expected.shape == result.shape


@pytest.mark.parametrize(
    "hour, expected",
    [
        (4, "Доброе утро"),
        (9, "Доброе утро"),
        (10, "Добрый день"),
        (16, "Добрый день"),
        (17, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
        (0, "Доброй ночи"),
        (3, "Доброй ночи"),
    ],
)
def test_greetings(hour, expected):
    assert greetings(datetime.datetime(2026, 1, 1, hour, 0, 0)) == expected


@pytest.mark.parametrize(
    "operations, date, expected",
    [
        (
            [
                {"Дата операции": "15.03.2024 10:30:00", "Сумма": 1000},
            ],
            "2024-03-20 00:00:00",
            [
                {"Дата операции": "15.03.2024 10:30:00", "Сумма": 1000},
            ],
        ),
        (
            [
                {"Дата операции": "15.03.2023 10:30:00", "Сумма": 1000},
            ],
            "2024-03-20 00:00:00",
            [],
        ),
        (
            [
                {"Дата операции": "15.04.2024 10:30:00", "Сумма": 1000},
            ],
            "2024-03-20 00:00:00",
            [],
        ),
        (
            [
                {"Дата операции": "25.03.2024 10:30:00", "Сумма": 1000},
            ],
            "2024-03-20 00:00:00",
            [],
        ),
        (
            [
                {"Дата операции": "10.03.2024 08:00:00", "Сумма": 500},
                {"Дата операции": "22.03.2024 14:15:00", "Сумма": 1200},
                {"Дата операции": "05.04.2024 09:45:00", "Сумма": 800},
            ],
            "2024-03-15 00:00:00",
            [
                {"Дата операции": "10.03.2024 08:00:00", "Сумма": 500},
            ],
        ),
        (
            [],
            "2024-03-20 00:00:00",
            [],
        ),
        (
            [
                {"Дата операции": "20.03.2024 12:00:00", "Сумма": 750},
            ],
            "2024-03-20 00:00:00",
            [
                {"Дата операции": "20.03.2024 12:00:00", "Сумма": 750},
            ],
        ),
        (
            [
                {"Дата операции": "01.03.2024 00:01:00", "Сумма": 200},
            ],
            "2024-03-05 00:00:00",
            [
                {"Дата операции": "01.03.2024 00:01:00", "Сумма": 200},
            ],
        ),
    ],
)
def test_operations_in_period(operations, date, expected):
    result = operations_in_period(operations, date)
    assert result == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [
                {"Номер карты": "1234567890123456", "Сумма операции": -1000.50, "Кэшбэк": 10.00},
                {"Номер карты": "1234567890123456", "Сумма операции": -500.25, "Кэшбэк": 5.25},
                {"Номер карты": "1234567890123456", "Сумма операции": 200.00, "Кэшбэк": 0.00},  # доход, не трата
            ],
            [
                {
                    "last_digits": "3456",
                    "total_spent": 1500.75,
                    "cashback": 15.25,
                }
            ],
        ),
        (
            [
                {"Номер карты": "1111222233334444", "Сумма операции": -200.00, "Кэшбэк": 4.00},
                {"Номер карты": "5555666677778888", "Сумма операции": -300.00, "Кэшбэк": 6.00},
                {"Номер карты": "1111222233334444", "Сумма операции": -150.75, "Кэшбэк": 3.00},
            ],
            [
                {
                    "last_digits": "4444",
                    "total_spent": 350.75,
                    "cashback": 7.00,
                },
                {
                    "last_digits": "8888",
                    "total_spent": 300.00,
                    "cashback": 6.00,
                },
            ],
        ),
        (
            [
                {"Номер карты": "9999888877776666", "Сумма операции": 500.00, "Кэшбэк": 10.00},  # доход
                {"Номер карты": "9999888877776666", "Сумма операции": 100.00, "Кэшбэк": 2.50},  # доход
            ],
            [
                {
                    "last_digits": "6666",
                    "total_spent": 0.00,
                    "cashback": 12.50,
                }
            ],
        ),
        (
            [
                {"Номер карты": "1234123412341234", "Сумма операции": -750.00, "Кэшбэк": 0.00},
                {
                    "Номер карты": "1234123412341234",
                    "Сумма операции": -250.00,
                    "Кэшбэк": -5.00,
                },
            ],
            [
                {
                    "last_digits": "1234",
                    "total_spent": 1000.00,
                    "cashback": 0.00,
                }
            ],
        ),
        (
            [],
            [],
        ),
        (
            [
                {"Номер карты": "0000111122223333", "Сумма операции": -42.80, "Кэшбэк": 0.85},
            ],
            [
                {
                    "last_digits": "3333",
                    "total_spent": 42.80,
                    "cashback": 0.85,
                }
            ],
        ),
        (
            [
                {"Номер карты": "1111111111111111", "Сумма операции": -100.00, "Кэшбэк": 2.00},
                {"Номер карты": "1111111111111111", "Сумма операции": -200.00, "Кэшбэк": 4.00},
            ],
            [
                {
                    "last_digits": "1111",
                    "total_spent": 300.00,
                    "cashback": 6.00,
                }
            ],
        ),
    ],
)
def test_cards(data, expected):
    result = cards(data)
    assert result == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [
                {
                    "Дата операции": "2024-01-15 10:30:00",
                    "Сумма операции": -1000.50,
                    "Категория": "Продукты",
                    "Описание": "Супермаркет",
                },
                {
                    "Дата операции": "2024-03-10 09:15:00",
                    "Сумма операции": -2000.00,
                    "Категория": "Одежда",
                    "Описание": "Магазин одежды",
                },
            ],
            [
                {"date": "2024-03-10", "amount": 2000.00, "category": "Одежда", "description": "Магазин одежды"},
                {"date": "2024-01-15", "amount": 1000.50, "category": "Продукты", "description": "Супермаркет"},
            ],
        ),
        (
            [
                {
                    "Дата операции": "2024-04-05 11:00:00",
                    "Сумма операции": -100.00,
                    "Категория": "Кафе",
                    "Описание": "Кофе",
                },
                {
                    "Дата операции": "2024-05-12 13:20:00",
                    "Сумма операции": -200.00,
                    "Категория": "Транспорт",
                    "Описание": "Такси",
                },
                {
                    "Дата операции": "2024-06-18 16:30:00",
                    "Сумма операции": -300.00,
                    "Категория": "Развлечения",
                    "Описание": "Кинотеатр",
                },
                {
                    "Дата операции": "2024-07-22 18:40:00",
                    "Сумма операции": -400.00,
                    "Категория": "Спорт",
                    "Описание": "Абонемент",
                },
                {
                    "Дата операции": "2024-08-30 20:50:00",
                    "Сумма операции": -500.00,
                    "Категория": "Электроника",
                    "Описание": "Наушники",
                },
            ],
            [
                {"date": "2024-08-30", "amount": 500.00, "category": "Электроника", "description": "Наушники"},
                {"date": "2024-07-22", "amount": 400.00, "category": "Спорт", "description": "Абонемент"},
                {"date": "2024-06-18", "amount": 300.00, "category": "Развлечения", "description": "Кинотеатр"},
                {"date": "2024-05-12", "amount": 200.00, "category": "Транспорт", "description": "Такси"},
                {"date": "2024-04-05", "amount": 100.00, "category": "Кафе", "description": "Кофе"},
            ],
        ),
        (
            [
                {
                    "Дата операции": "2024-01-01 08:00:00",
                    "Сумма операции": -50.00,
                    "Категория": "Связь",
                    "Описание": "Оплата телефона",
                },
                {
                    "Дата операции": "2024-02-02 09:15:00",
                    "Сумма операции": -150.00,
                    "Категория": "ЖКХ",
                    "Описание": "Коммуналка",
                },
                {
                    "Дата операции": "2024-03-03 10:30:00",
                    "Сумма операции": -250.00,
                    "Категория": "Аптека",
                    "Описание": "Лекарства",
                },
                {
                    "Дата операции": "2024-04-04 11:45:00",
                    "Сумма операции": -350.00,
                    "Категория": "Авто",
                    "Описание": "Топливо",
                },
                {
                    "Дата операции": "2024-05-05 13:00:00",
                    "Сумма операции": -450.00,
                    "Категория": "Путешествия",
                    "Описание": "Отель",
                },
                {
                    "Дата операции": "2024-06-06 14:15:00",
                    "Сумма операции": -550.00,
                    "Категория": "Обучение",
                    "Описание": "Курс",
                },
                {
                    "Дата операции": "2024-07-07 15:30:00",
                    "Сумма операции": -650.00,
                    "Категория": "Подарки",
                    "Описание": "День рождения",
                },
            ],
            [
                {"date": "2024-07-07", "amount": 650.00, "category": "Подарки", "description": "День рождения"},
                {"date": "2024-06-06", "amount": 550.00, "category": "Обучение", "description": "Курс"},
                {"date": "2024-05-05", "amount": 450.00, "category": "Путешествия", "description": "Отель"},
                {"date": "2024-04-04", "amount": 350.00, "category": "Авто", "description": "Топливо"},
                {"date": "2024-03-03", "amount": 250.00, "category": "Аптека", "description": "Лекарства"},
            ],
        ),
        (
            [
                {
                    "Дата операции": "2024-01-10 12:00:00",
                    "Сумма операции": 1000.00,
                    "Категория": "Зарплата",
                    "Описание": "Оклад",
                },
                {
                    "Дата операции": "2024-02-10 13:00:00",
                    "Сумма операции": -500.00,
                    "Категория": "Продукты",
                    "Описание": "Магазин",
                },
            ],
            [
                {"date": "2024-01-10", "amount": 1000.00, "category": "Зарплата", "description": "Оклад"},
                {"date": "2024-02-10", "amount": 500.00, "category": "Продукты", "description": "Магазин"},
            ],
        ),
        (
            [],
            [],
        ),
        (
            [
                {
                    "Дата операции": "2024-12-25 18:00:00",
                    "Сумма операции": -750.25,
                    "Категория": "Праздники",
                    "Описание": "Подарок",
                },
            ],
            [
                {"date": "2024-12-25", "amount": 750.25, "category": "Праздники", "description": "Подарок"},
            ],
        ),
        (
            [
                {"Дата операции": "2024-01-01 00:00:00", "Сумма операции": -100.00, "Категория": "А", "Описание": "1"},
                {"Дата операции": "2024-02-02 00:00:00", "Сумма операции": -100.00, "Категория": "Б", "Описание": "2"},
                {"Дата операции": "2024-03-03 00:00:00", "Сумма операции": -100.00, "Категория": "В", "Описание": "3"},
                {"Дата операции": "2024-04-04 00:00:00", "Сумма операции": -100.00, "Категория": "Г", "Описание": "4"},
                {"Дата операции": "2024-05-05 00:00:00", "Сумма операции": -100.00, "Категория": "Д", "Описание": "5"},
                {"Дата операции": "2024-06-06 00:00:00", "Сумма операции": -100.00, "Категория": "Е", "Описание": "6"},
            ],
            [
                {"date": "2024-01-01", "amount": 100.00, "category": "А", "description": "1"},
                {"date": "2024-02-02", "amount": 100.00, "category": "Б", "description": "2"},
                {"date": "2024-03-03", "amount": 100.00, "category": "В", "description": "3"},
                {"date": "2024-04-04", "amount": 100.00, "category": "Г", "description": "4"},
                {"date": "2024-05-05", "amount": 100.00, "category": "Д", "description": "5"},
            ],
        ),
        (
            [
                {
                    "Дата операции": "2024-07-07 09:00:00",
                    "Сумма операции": -123.456,
                    "Категория": "Разное",
                    "Описание": "Мелкая покупка",
                },
                {
                    "Дата операции": "2024-08-08 10:00:00",
                    "Сумма операции": -987.654,
                    "Категория": "Крупное",
                    "Описание": "Большая покупка",
                },
            ],
            [
                {"date": "2024-08-08", "amount": 987.65, "category": "Крупное", "description": "Большая покупка"},
                {"date": "2024-07-07", "amount": 123.46, "category": "Разное", "description": "Мелкая покупка"},
            ],
        ),
    ],
)
def test_top_5_transactions(data, expected):
    result = top_5_transactions(data)
    assert result == expected


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
@patch("requests.request")
def test_exchange_rate_success(mock_request, mock_open_func):

    response_usd = MagicMock()
    response_usd.status_code = 200
    response_usd.text = '{"result": 95.12345}'

    response_eur = MagicMock()
    response_eur.status_code = 200
    response_eur.text = '{"result": 102.45123}'

    mock_request.side_effect = [response_usd, response_eur]

    result = exchange_rate("dummy.json")
    expected = [
        {"currency": "USD", "rate": 95.12},
        {"currency": "EUR", "rate": 102.45},
    ]
    assert result == expected


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "MSFT"]}')
@patch("os.getenv", return_value="test_api_key_123")
@patch("requests.get")
def test_stock_price_success(mock_get, mock_getenv, mock_open_func):

    response_aapl = MagicMock()
    response_aapl.status_code = 200
    response_aapl.json = lambda: {"Time Series (Daily)": {"2024-04-10": {"4. close": "175.421"}}}

    response_msft = MagicMock()
    response_msft.status_code = 200
    response_msft.json = lambda: {"Time Series (Daily)": {"2024-04-10": {"4. close": "412.876"}}}

    mock_get.side_effect = [response_aapl, response_msft]

    result = stock_price("dummy_path.json")
    expected = [
        {"stock": "AAPL", "price": 175.42},
        {"stock": "MSFT", "price": 412.88},  # округление до 2 знаков
    ]
    assert result == expected
