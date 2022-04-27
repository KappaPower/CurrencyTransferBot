import requests
import json
from config import keys


class ConversionExeption(Exception):
    pass


class CurrencyTransfer:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionExeption(f'Одинаковые валюты: {base}')
        if ',' in amount:
            amount = amount.replace(',', '.')

        if float(amount) < 0:
            raise ConversionExeption('Нельзя перевести отрицательное число')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExeption(f'Неверное количество {amount}')

        r = requests.get(f"https://www.cbr-xml-daily.ru/latest.js")
        resp = json.loads(r.content)
        if base_ticker == 'RUB':
            new_price = (1 / resp['rates'][quote_ticker]) * float(amount)
        elif quote_ticker == 'RUB':
            new_price = resp['rates'][base_ticker] * float(amount)
        else:
            new_price = resp['rates'][base_ticker] * float(amount) * (1 / resp['rates'][quote_ticker])
        new_price = round(new_price, 3)
        message = f"Цена {amount} {quote_ticker} в {base_ticker} : {new_price}"
        return message
