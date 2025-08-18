# utils.py


from datetime import datetime
import pandas as pd
import requests
from pandas import DataFrame
import json


URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = "QM1GnBohgzwIoVigK2I4ttSv86H0VoFD"
STOCK_API_URL = 'https://www.alphavantage.co/query'
STOCK_API_KEY = '<YOUR_ALPHA_VANTAGE_API_KEY>'

def get_time_for_greeting():
   """
     Функция возращает приветствие
     в зависимости от текущего времени
   """
   user_datetime_hour = datetime.now().hour
   if 5 <= user_datetime_hour < 12:
     return "Доброе утро"
   elif  12 <= user_datetime_hour < 18:
     return "Добрый день"
   elif  18 <= user_datetime_hour < 23:
     return "Добрый вечер"
   else:
     return "Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [
        start_of_month.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]

def get_path_and_period(path_to_file: str, period_date: list) -> DataFrame:
    """
        Функция принимает путь к Excel файлу, и список дат, и возвращает
        таблицу в заданном периоде
    """
    df= pd.read_excel(path_to_file, sheet_name="Отчет по операциям")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
    ]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
        Функция принимает DataFrame и возвращает список карт с расходами и кэшбеком
    """
    card_spend_transactions = []
    card_sorted = sorted_df[
        ["Номер карты",
         "Сумма операции",
         "Кэшбэк",
         "Сумма операции с округлением"
         ]
    ]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent // 100
            row = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback
            }
            card_spend_transactions.append(row)
    return card_spend_transactions


def get_top_transactions(sorted_df: DataFrame, get_top):
    """
        Функция принимает DataFrame и возвращает топ-транзакций по сумме платежа
    """
    top_pay_transactions =[]
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]

    for index, row in top_transactions_sorted.iterrows():
        transaction = {
            "date": f"{row['Дата платежа']}",
            "amount": f"{row['Сумма операции']}",
            "category": f"{row['Категория']}",
            "description": f"{row['Описание']}"
        }
        top_pay_transactions.append(transaction)

    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict]:
    """
        Функция принимает на вход путь к json и возвращает курс валют
    """
    currency_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currencys = data['user_currencies']

        for currency in currencys:
            params = {
                "amount": 1,
                "from": f"{currency}",
                "to": f"RUB"
            }
            headers = {
                "apikey": f"{API_KEY}"
            }
            response = requests.request("GET", URL, headers=headers, data=params)

            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                currency_code_response = result["query"]["from"]
                currency_amount = round(result["result"], 2)
                currency_rates.append({
                    "currency": f"{currency_code_response}",
                    "rate": f"{currency_amount}"
                })

        return currency_rates


def get_stock(path_to_json: str) -> list[dict]:
    """
           Функция принимает на вход путь к json и возвращает цену акции
       """
    stock_prices = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data['user_stocks']

        for stock in stocks:
            # Запрашиваем последнюю цену акции
            payload = {
                'function': 'GLOBAL_QUOTE',
                'symbol': stock,
                'apikey': STOCK_API_KEY
            }
            response = requests.get(STOCK_API_URL, params=payload)
            try:
                data = response.json()['Global Quote']['05. price']
                stock_prices.append({'stock': stock, 'price': float(data)})
            except KeyError:
                print(f'Ошибка при получении данных для {stock}')

        return stock_prices



