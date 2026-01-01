import datetime
import functools
import logging
from typing import Callable, Optional, ParamSpec, TypeVar

import pandas as pd  # type: ignore[import]

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


def save_report_to_file(filename: Optional[str] = None) -> Callable[[Callable[P, T]], Callable[P, T]] | str:
    """
    Декоратор, сохраняющий результат функции в текстовый файл.

    Параметры:
        filename (str, optional): имя файла для сохранения результата.
            Если None (по умолчанию), генерируется автоматическое имя в формате:
            "report_ГГГГ‑ММ‑ДД_ЧЧ‑ММ‑СС.txt" с текущей датой и временем.

    Возвращаемое значение:
        Callable[[Callable[P, T]], Callable[P, T]]: декоратор, который:
            - принимает функцию типа Callable[P, T];
            - возвращает функцию того же типа Callable[P, T],
              добавляя логику сохранения результата в файл.
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции save_report_to_file")

    try:

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                result = func(*args, **kwargs)
                if filename is None:
                    file_name = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
                else:
                    file_name = filename

                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(str(result))
                return result

            return wrapper

        logger.info("Вывод результатов работы функции save_report_to_file")
        return decorator

    except Exception as E:
        logger.error(f"Ошибка {E} в функции save_report_to_file")
        return ""


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | str:
    """
    Рассчитывает суммарные траты по заданной категории за последние 3 месяца относительно указанной даты.

    Параметры:
        transactions (pd.DataFrame): датафрейм с транзакциями. Должен содержать столбцы:
            - "Категория" (str): категория операции;
            - "Дата операции" (str/datetime): дата операции (формат ДД.ММ.ГГГГ или аналогичный);
            - "Сумма операции" (float/int): сумма операции (отрицательные значения — расходы).
        category (str): название категории, по которой требуется рассчитать траты.
        date (str, optional): опорная дата в формате "ДД.ММ.ГГГГ" или подобном.
            Если не указана, используется текущая дата.

    Возвращаемое значение:
        float: суммарные траты (сумма значений "Сумма операции") по указанной категории
            за период: [дата − 3 месяца; дата].
            Если подходящих транзакций нет — возвращается 0.0.
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции spending_by_category")

    try:
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

        logger.info("Вывод результатов работы функции spending_by_category")
        return round(filtered_transactions["Сумма операции"].sum(), 2)

    except Exception as E:
        logger.error(f"Ошибка {E} в функции spending_by_category")
        return ""
