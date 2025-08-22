import pytest
from unittest.mock import patch
from datetime import datetime
import pandas as pd
import json
import pytest
import tempfile


from src.utils import get_time_for_greeting
@pytest.mark.parametrize("current_hour, expected_greeting", [
    (7, "Доброе утро"),
    (10, "Доброе утро"),
    (12, "Добрый день"),
    (15, "Добрый день"),
    (19, "Добрый вечер"),
    (21, "Добрый вечер"),
    (23, "Доброй ночи"),
    (3, "Доброй ночи")
])
@patch('src.utils.datetime')
def test_get_time_for_greeting(mocked_datetime, current_hour, expected_greeting):
    # Настройка mock объекта для возврата заданного часа
    mocked_datetime.now.return_value.hour = current_hour

    result = get_time_for_greeting()

    assert result == expected_greeting


from src.utils import get_data_time
# Тестируем стандартную ситуацию
def test_get_data_time_standard_case():
    input_date_time = '2023-10-15 12:34:56'
    output = get_data_time(input_date_time)
    expected_output = ['01.10.2023 12:34:56', '15.10.2023 12:34:56']
    assert output == expected_output


# Проверяем случай, когда дата находится в конце месяца
def test_get_data_time_end_of_month():
    input_date_time = '2023-12-31 23:59:59'
    output = get_data_time(input_date_time)
    expected_output = ['01.12.2023 23:59:59', '31.12.2023 23:59:59']
    assert output == expected_output


# Проверяем начало нового года
def test_get_data_time_new_year():
    input_date_time = '2024-01-01 00:00:00'
    output = get_data_time(input_date_time)
    expected_output = ['01.01.2024 00:00:00', '01.01.2024 00:00:00']
    assert output == expected_output


# Проверяем нестандартный формат даты-времени
def test_get_data_time_custom_format():
    input_date_time = '2023-10-15T12:34:56Z'  # ISO format
    custom_format = '%Y-%m-%dT%H:%M:%SZ'
    output = get_data_time(input_date_time, custom_format)
    expected_output = ['01.10.2023 12:34:56', '15.10.2023 12:34:56']
    assert output == expected_output


# Проверяем некорректный ввод формата
def test_get_data_time_invalid_input():
    with pytest.raises(ValueError):
        get_data_time('invalid string', '%Y-%m-%d %H:%M:%S')


from src.utils import get_path_and_period
# Используем фикстуру, чтобы создать тестовый Excel-файл перед каждым тестом
@pytest.fixture(scope="module")
def create_test_excel(tmpdir_factory):
    data = {
        "Дата операции": ["01.01.2023 12:00:00", "02.01.2023 12:00:00",
                         "03.01.2023 12:00:00", "04.01.2023 12:00:00"],
        "Сумма": [100, 200, 300, 400],
    }
    df = pd.DataFrame(data)
    file_path = tmpdir_factory.mktemp("data").join("test.xlsx")
    df.to_excel(file_path, index=False, sheet_name="Отчет по операциям")
    return str(file_path)

# Тест проверки чтения файла и фильтрации по простейшему периоду
def test_get_path_and_period_simple(create_test_excel):
    path_to_file = create_test_excel
    period_date = ["01.01.2023 12:00:00", "02.01.2023 12:00:00"]
    result = get_path_and_period(path_to_file, period_date)
    expected_dates = [pd.Timestamp("2023-01-01 12:00:00"), pd.Timestamp("2023-01-02 12:00:00")]
    assert len(result) == 2
    assert all([result["Дата операции"].iloc[i] == expected_dates[i] for i in range(len(expected_dates))])

# Тест проверки сортировки результатов
def test_get_path_and_period_sorting(create_test_excel):
    path_to_file = create_test_excel
    period_date = ["01.01.2023 12:00:00", "04.01.2023 12:00:00"]
    result = get_path_and_period(path_to_file, period_date)
    expected_order = ["01.01.2023 12:00:00", "02.01.2023 12:00:00", "03.01.2023 12:00:00", "04.01.2023 12:00:00"]
    actual_order = result["Дата операции"].dt.strftime('%d.%m.%Y %H:%M:%S').tolist()
    assert actual_order == expected_order

# Тест проверки поведения при пустых результатах
def test_get_path_and_period_empty_result(create_test_excel):
    path_to_file = create_test_excel
    period_date = ["05.01.2023 12:00:00", "06.01.2023 12:00:00"]  # Период вне реальных данных
    result = get_path_and_period(path_to_file, period_date)
    assert len(result) == 0

# Тест проверки поведения при передаче неправильного пути к файлу
def test_get_path_and_period_wrong_path():
    wrong_path = "/path/to/nonexistent/file.xlsx"
    period_date = ["01.01.2023 12:00:00", "02.01.2023 12:00:00"]
    with pytest.raises(FileNotFoundError):
        get_path_and_period(wrong_path, period_date)

# Тест проверки периода с неправильным форматом даты
def test_get_path_and_period_incorrect_date_format(create_test_excel):
    path_to_file = create_test_excel
    incorrect_period = ["01-01-2023 12:00:00", "02-01-2023 12:00:00"]  # Неправильный формат даты
    with pytest.raises(ValueError):
        get_path_and_period(path_to_file, incorrect_period)



from src.utils import get_card_with_spend
def prepare_test_dataframe():
    data = {
        "Номер карты": ["*1234", "*5678", "*9012"],
        "Сумма операции": [-1000, -2000, 3000],  # Расходы имеют отрицательные суммы
        "Кэшбэк": [10, 20, 30],
        "Сумма операции с округлением": [-1000, -2000, 3000]
    }
    return pd.DataFrame(data)

def test_get_card_with_spend_basic(prepare_test_dataframe):
    df = prepare_test_dataframe()
    result = get_card_with_spend(df)

    expected_result = [
        {"last_digits": "1234", "total_spent": -1000, "cashback": -10},
        {"last_digits": "5678", "total_spent": -2000, "cashback": -20}
    ]

    assert result == expected_result

def test_get_card_with_spend_no_expenses(prepare_test_dataframe):
    df = prepare_test_dataframe()
    df["Сумма операции"] = [3000, 4000, 5000]  # Все доходы
    result = get_card_with_spend(df)

    assert result == []  # Ожидаемый пустой список

def test_get_card_with_spend_masked_card_number(prepare_test_dataframe):
    df = prepare_test_dataframe()
    df.at[0, "Номер карты"] = "*1234"
    df.at[1, "Номер карты"] = "*5678"
    df.at[2, "Номер карты"] = "*9012"

    result = get_card_with_spend(df)

    expected_result = [
        {"last_digits": "1234", "total_spent": -1000, "cashback": -10},
        {"last_digits": "5678", "total_spent": -2000, "cashback": -20}
    ]

    assert result == expected_result

def test_get_card_with_spend_missing_columns():
    df = pd.DataFrame({"Неправильные_колонки": [1, 2, 3]})
    with pytest.raises(KeyError):
        get_card_with_spend(df)


from src.utils import get_top_transactions

@pytest.fixture
def prepare_test_dataframe():
    data = {
        "Номер карты": ["*1234", "*5678", "*9012"],
        "Сумма операции": [-1000, -2000, 3000],
        "Кэшбэк": [10, 20, 30],
        "Сумма операции с округлением": [-1000, -2000, 3000]
    }
    return pd.DataFrame(data)

def prepare_test_dataframe():
    data = {
        "Дата платежа": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "Сумма операции": [1000, 2000, 3000, 4000],
        "Категория": ["Продукты", "Одежда", "Транспорт", "Рестораны"],
        "Описание": ["Покупка продуктов", "Новая одежда", "Поездка на такси", "Обед в ресторане"]
    }
    return pd.DataFrame(data)


def test_get_top_transactions_basic(prepare_test_dataframe):
    df = prepare_test_dataframe()
    result = get_top_transactions(df, 2)

    expected_result = [
        {'date': '2023-01-04', 'amount': '4000', 'category': 'Рестораны', 'description': 'Обед в ресторане'},
        {'date': '2023-01-03', 'amount': '3000', 'category': 'Транспорт', 'description': 'Поездка на такси'}
    ]

    assert result == expected_result

def test_get_top_transactions_all(prepare_test_dataframe):
    df = prepare_test_dataframe()
    result = get_top_transactions(df, 4)

    expected_result = [
        {'date': '2023-01-04', 'amount': '4000', 'category': 'Рестораны', 'description': 'Обед в ресторане'},
        {'date': '2023-01-03', 'amount': '3000', 'category': 'Транспорт', 'description': 'Поездка на такси'},
        {'date': '2023-01-02', 'amount': '2000', 'category': 'Одежда', 'description': 'Новая одежда'},
        {'date': '2023-01-01', 'amount': '1000', 'category': 'Продукты', 'description': 'Покупка продуктов'}
    ]

    assert result == expected_result

def test_get_top_transactions_negative_count(prepare_test_dataframe):
    df = prepare_test_dataframe()
    with pytest.raises(ValueError):
        get_top_transactions(df, -1)

def test_get_top_transactions_empty_df():
    empty_df = pd.DataFrame(columns=["Дата платежа", "Сумма операции", "Категория", "Описание"])
    result = get_top_transactions(empty_df, 2)

    assert result == []



from src.utils import get_stock

@pytest.fixture
def sample_json(tmp_path):
    data = {
        "user_stocks": ["AAPL", "GOOG"]
    }
    json_file = tmp_path / "stocks.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return str(json_file)


import requests_mock

@pytest.fixture
def mock_api_request():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def mock_api_response(mock_api_request):
    mock_api_request.get(
        requests_mock.ANY,
        json={
            "Global Quote": {
                "05. price": "100.00"
            }
        },
        status_code=200
    )

def test_get_stock_success(sample_json, mock_api_response):
    result = get_stock(sample_json)

    expected_result = [
        {"stock": "AAPL", "price": 100.0},
        {"stock": "GOOG", "price": 100.0}
    ]

    assert result == expected_result

def test_get_stock_file_not_found():
    nonexistent_path = "/path/to/nonexistent/file.json"
    with pytest.raises(FileNotFoundError):
        get_stock(nonexistent_path)

@pytest.fixture
def mock_bad_status_api_response(mock_api_request):
    mock_api_request.get(
        requests_mock.ANY,
        text='Bad Request',
        status_code=400
    )

def test_get_stock_bad_status(sample_json, mock_bad_status_api_response):
    result = get_stock(sample_json)
    assert len(result) == 0