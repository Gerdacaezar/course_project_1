import json

from src.services import cashback_categories


def test_cashback_categories_success(sample_data):
    result = cashback_categories(sample_data, 2024, 1)
    parsed_result = json.loads(result)
    expected = {
        "Продукты": 15,
        "Развлечения": 8,
        "Транспорт": 3,
    }

    assert parsed_result == expected


def test_cashback_categories_empty_month(sample_data):
    result = cashback_categories(sample_data, 2024, 3)
    parsed_result = json.loads(result)
    assert parsed_result == {}


def test_cashback_categories_single_category(sample_data):
    filtered_data = [op for op in sample_data if op["Категория"] == "Транспорт" and "01.2024" in op["Дата операции"]]
    result = cashback_categories(filtered_data, 2024, 1)
    parsed_result = json.loads(result)
    expected = {"Транспорт": 3}
    assert parsed_result == expected


def test_cashback_categories_sorting(sample_data):
    result = cashback_categories(sample_data, 2024, 1)
    parsed_result = json.loads(result)
    values = list(parsed_result.values())
    assert values == sorted(values, reverse=True)


def test_cashback_categories_string_year_month(sample_data):
    result = cashback_categories(sample_data, "2024", "1")
    parsed_result = json.loads(result)

    expected = {
        "Продукты": 15,
        "Развлечения": 8,
        "Транспорт": 3,
    }

    assert parsed_result == expected
