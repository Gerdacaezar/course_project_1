import json

from src.utils import (cards, exchange_rate, greetings, operations_in_period, stock_price, top_5_transactions,
                       xlsx_to_list_of_dict)


def home_page(date_time: str) -> str:
    """Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ"""
    data = operations_in_period(xlsx_to_list_of_dict("../data/operations.xlsx"), date_time)

    result = {
        "greeting": greetings(),
        "cards": cards(data),
        "top_transactions": top_5_transactions(data),
        "currency_rates": exchange_rate("../user_settings.json"),
        "stock_prices": stock_price("../user_settings.json"),
    }

    json_data = json.dumps(result, indent=4, ensure_ascii=False)
    return json_data


# print(home_page('2019-03-03 12:12:12'))
