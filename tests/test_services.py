import pandas as pd
import numpy as np
import pytest
from src.services import anylize_cashback

@pytest.fixture
def test_dataframe():
    data = {
        "Дата операции": ["01.01.2023 12:00:00", "02.01.2023 13:00:00", "03.01.2023 14:00:00", "04.01.2023 15:00:00"],
        "Сумма платежа": [-1000, -2000, 3000, -4000],
        "Кэшбэк": [10, 20, 0, 40],
        "Категория": ["Магазины", "Путешествия", "Заработок", "Магазины"]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    return df


def test_anylize_cashback(test_dataframe, tmp_path):
    temp_excel = tmp_path / "test.xlsx"
    test_dataframe.to_excel(temp_excel, index=False)

    result = anylize_cashback(str(temp_excel), 2023, 1)

    expected_result = '{"Магазины": 50}'

    assert result.strip() == expected_result.strip()


def test_anylize_cashback_no_cashback(test_dataframe, tmp_path):
    test_dataframe["Кэшбэк"] = 0
    temp_excel = tmp_path / "test.xlsx"
    test_dataframe.to_excel(temp_excel, index=False)

    result = anylize_cashback(str(temp_excel), 2023, 1)

    expected_result = '{}'

    assert result.strip() == expected_result.strip()


def test_anylize_cashback_different_years_and_months(test_dataframe, tmp_path):
    test_dataframe.loc[0, "Дата операции"] = "01.02.2023 12:00:00"
    temp_excel = tmp_path / "test.xlsx"
    test_dataframe.to_excel(temp_excel, index=False)

    result = anylize_cashback(str(temp_excel), 2023, 1)

    expected_result = '{}'

    assert result.strip() == expected_result.strip()