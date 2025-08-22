import pytest
import json
from unittest.mock import patch, MagicMock
from src.views import main_info

@pytest.fixture
def sample_datetime():
    return "2018-05-20 15:30:00"

@pytest.fixture
def mock_dependencies():
    # Можем замочить все вызовы внутренних методов
    with patch.multiple(
        "main_function",
        get_data_time=MagicMock(return_value=None),
        get_path_and_period=MagicMock(return_value=[]),
        get_time_for_greeting=MagicMock(return_value="Привет!"),
        get_card_with_spend=MagicMock(return_value=[]),
        get_top_transactions=MagicMock(return_value=[]),
        get_currency=MagicMock(return_value=[]),
        get_stock=MagicMock(return_value=[])
    ) as mocks:
        yield mocks

def test_main_info_base_case(sample_datetime, mock_dependencies):
    result = main_info(sample_datetime)

    # Проверим структуру возвращённого JSON
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, dict)
    assert "greeting" in parsed_result
    assert "cards" in parsed_result
    assert "top_transactions" in parsed_result
    assert "currency_rates" in parsed_result
    assert "stock_prices" in parsed_result


def test_main_info_json_structure(sample_datetime, mock_dependencies):
    result = main_info(sample_datetime)
    parsed_result = json.loads(result)

    # Оценим структуру полученных данных
    assert isinstance(parsed_result["greeting"], str)
    assert isinstance(parsed_result["cards"], list)
    assert isinstance(parsed_result["top_transactions"], list)
    assert isinstance(parsed_result["currency_rates"], list)
    assert isinstance(parsed_result["stock_prices"], list)


def test_main_info_invalid_datetime():
    invalid_datetime = "abc"
    with pytest.raises(Exception):
        main_info(invalid_datetime)