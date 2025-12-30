import datetime
import functools
from typing import Callable, Optional

import pandas as pd  # type: ignore[import]


def save_report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения результата функции-отчёта в файл.

    Варианты использования:
    - @save_report_to_file()          # имя файла по умолчанию
    - @save_report_to_file("my_report.txt")  # указанное имя файла

    Параметры:
        filename (str, optional): имя файла для сохранения. Если None — генерируется автоматически.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Callable, **kwargs: Callable) -> Callable:
            result = func(*args, **kwargs)

            if filename is None:
                file_name = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            else:
                file_name = filename

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(str(result))

            return result

        return wrapper

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает на вход:
            датафрейм с транзакциями,
            название категории,
            опциональную дату.
        Если дата не передана, то берется текущая дата.

    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    now = datetime.datetime.now()
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    if not date:
        end_date = now
        start_date = now - pd.DateOffset(months=3)
    else:
        input_date = pd.to_datetime(date, dayfirst=True)
        end_date = input_date
        start_date = input_date - pd.DateOffset(months=3)

    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]
    return filtered_transactions["Сумма операции"].sum()
