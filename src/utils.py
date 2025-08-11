# utils.py


from datetime import datetime


def get_time_for_greeting():
   """
     Функция возращает приветствие
     в зависимости от текущего времени
   """
   user_datetime = datetime.now()
   hour = user_datetime.hour
   if 5 <= hour < 12:
     return "Доброе утро"
   elif  12 <= hour < 18:
     return "Добрый день"
   elif  18 <= hour < 23:
     return "Добрый вечер"
   else:
     return "Доброй ночи"


# views.py

from typing import Dict, Any
from src.utils import get_time_for_greeting


def main_info() -> Dict[str, Any]:

    # 1. Приветствие
    greeting = get_time_for_greeting()

    # 2. По каждой карте

    # 3. Топ-5 транзакций по сумме платежа

    # 4. Курс валют

    # 5. Стоимость акций из S&P500

    json_data = {
          "greeting": greeting,
          "cards": [
            {
              "last_digits": "5814",
              "total_spent": 1262.00,
              "cashback": 12.62
            },
            {
              "last_digits": "7512",
              "total_spent": 7.94,
              "cashback": 0.08
            }
          ],
          "top_transactions": [
            {
              "date": "21.12.2021",
              "amount": 1198.23,
              "category": "Переводы",
              "description": "Перевод Кредитная карта. ТП 10.2 RUR"
            },
            {
              "date": "20.12.2021",
              "amount": 829.00,
              "category": "Супермаркеты",
              "description": "Лента"
            },
            {
              "date": "20.12.2021",
              "amount": 421.00,
              "category": "Различные товары",
              "description": "Ozon.ru"
            },
            {
              "date": "16.12.2021",
              "amount": -14216.42,
              "category": "ЖКХ",
              "description": "ЖКУ Квартира"
            },
            {
              "date": "16.12.2021",
              "amount": 453.00,
              "category": "Бонусы",
              "description": "Кешбэк за обычные покупки"
            }
          ],
          "currency_rates": [
            {
              "currency": "USD",
              "rate": 73.21
            },
            {
              "currency": "EUR",
              "rate": 87.08
            }
          ],
          "stock_prices": [
            {
              "stock": "AAPL",
              "price": 150.12
            },
            {
              "stock": "AMZN",
              "price": 3173.18
            },
            {
              "stock": "GOOGL",
              "price": 2742.39
            },
            {
              "stock": "MSFT",
              "price": 296.71
            },
            {
              "stock": "TSLA",
              "price": 1007.08
            }
          ]
    }

    return json_data

from pprint import pprint

if __name__ == "__main__":
  pprint(main_info())