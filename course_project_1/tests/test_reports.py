import os

import pandas as pd

from src.reports import save_report_to_file, spending_by_category


def test_save_report_to_file_success():
    @save_report_to_file("test_report.txt")
    def get_report():
        return "Это содержимое отчёта"

    result = get_report()
    assert result == "Это содержимое отчёта"
    assert os.path.isfile("test_report.txt")
    with open("test_report.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "Это содержимое отчёта"

    os.remove("test_report.txt")


def test_spending_by_category_success():
    test_data = pd.DataFrame(
        {
            "Дата операции": [
                "01.01.2025",
                "15.02.2025",
                "10.03.2025",
                "20.04.2025",
                "05.12.2024",
            ],
            "Категория": ["Продукты", "Продукты", "Продукты", "Продукты", "Продукты"],
            "Сумма операции": [-1000, -2000, -1500, -500, -300],
        }
    )

    result = spending_by_category(test_data, "Продукты", "01.04.2025")
    assert result == -4500
