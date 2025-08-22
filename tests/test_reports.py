import pandas as pd
import pytest
from src.reports import spending_by_category

@pytest.fixture
def transactions_df():
    data = {
        'Дата операции': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'Сумма': [-1000, -2000, -3000, -4000],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Жильё']
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    return df

def test_spending_by_category_standard(transactions_df):
    result = spending_by_category(transactions_df, 'Еда', '2023-03-01')
    expected_result = {'Еда': -4000}
    assert result == expected_result

def test_spending_by_category_no_category(transactions_df):
    result = spending_by_category(transactions_df, 'Спорт', '2023-03-01')
    expected_result = {}
    assert result == expected_result

def test_spending_by_category_invalid_date(transactions_df):
    with pytest.raises(ValueError):
        spending_by_category(transactions_df, 'Еда', '2023-13-01')

def test_spending_by_category_edge_case(transactions_df):
    result = spending_by_category(transactions_df, 'Еда', '2023-01-01')
    expected_result = {'Еда': -1000}
    assert result == expected_result