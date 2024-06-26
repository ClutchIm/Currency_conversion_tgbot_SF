import requests
import json
from config import keys


class ApiException(Exception):
    pass


class CurrencyExchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ApiException(f'Невозможно конвертировать одинаковые валюты = {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        unit_cost = json.loads(r.content)[keys[base]]
        total_base = unit_cost * amount

        return total_base
