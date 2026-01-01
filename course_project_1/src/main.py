import logging

from config.logging_config import setup_logging
from src.reports import spending_by_category
from src.services import cashback_categories
from src.utils import xlsx_to_dataframe, xlsx_to_list_of_dict
from src.views import home_page


def main() -> str:
    """
    Основная функция запуска приложения.

    Выполняет последовательный вызов ключевых функций проекта с логированием этапов выполнения
    и обработкой возможных исключений. Результаты объединяются в итоговую строку.

    Параметры:
        Нет. Функция не принимает аргументов.

    Возвращаемое значение:
        str: объединённая строка с результатами выполнения трёх основных функций:
            - home_page
            - cashback_categories
            - spending_by_category
        При возникновении ошибки возвращает пустую строку ''.
    """

    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Приложение запущено")

    try:
        logger.info("Запуск функции home_page")
        home_page_module = home_page("2019-03-03 12:12:12")

        logger.info("Запуск функции cashback_categories")
        cashback_categories_module = cashback_categories(xlsx_to_list_of_dict("../data/operations.xlsx"), 2019, 1)

        logger.info("Запуск функции spending_by_category")
        spending_by_category_module = spending_by_category(
            xlsx_to_dataframe("../data/operations.xlsx"), "Супермаркеты", "2019-03-03"
        )

        logger.info("Вывод результатов работы функции main")
        return f"""
        {print(home_page_module)}
        {print(cashback_categories_module)}
        {print(spending_by_category_module)}"""

    except Exception as E:
        logger.error(f"Ошибка {E} в функции main")
        return ""


if __name__ == "__main__":
    main()
