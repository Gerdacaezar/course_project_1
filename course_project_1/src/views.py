import json
import logging

from src.utils import (cards, exchange_rate, greetings, operations_in_period, stock_price, top_5_transactions,
                       xlsx_to_list_of_dict)

logger = logging.getLogger(__name__)


def home_page(date_time: str) -> str:
    """
    Формирует JSON‑строку с данными для главной страницы личного кабинета.

    Параметры:
        date_time (str): опорная дата и время в формате "ГГГГ‑ММ‑ДД ЧЧ:ММ:СС",
            относительно которой фильтруются операции (например, "2025‑01‑15 14:30:00").

    Возвращаемое значение:
        str: JSON‑строка с комплексной информацией для отображения на главной странице.
            Содержит следующие ключи:
            - "greeting" (str): приветствие в зависимости от времени суток;
            - "cards" (list[dict]): сводная статистика по банковским картам (расходы и кэшбэк);
            - "top_transactions" (list[dict]): топ‑5 транзакций по сумме;
            - "currency_rates" (list[dict]): текущие курсы валют к рублю;
            - "stock_prices" (list[dict]): текущие цены акций.
        При возникновении ошибки возвращает пустую строку ''.
    """
    logger.info("Запуск функции home_page")
    try:
        data = operations_in_period(xlsx_to_list_of_dict("../data/operations.xlsx"), date_time)

        result = {
            "greeting": greetings(),
            "cards": cards(data),
            "top_transactions": top_5_transactions(data),
            "currency_rates": exchange_rate("../user_settings.json"),
            "stock_prices": stock_price("../user_settings.json"),
        }

        json_data = json.dumps(result, indent=4, ensure_ascii=False)
        logger.info("Вывод результата работы функции home_page")
        return json_data
    except Exception as E:
        logger.error(f"Ошибка {E} в функции home_page")
        return ""
