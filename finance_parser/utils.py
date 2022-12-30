import requests
from finance_parser.db.session import SessionLocal
from typing import Generator


def get_data_from_alphavintage_full(symbol, interval, api_key):
    print(f"requesting symbol \"{symbol}\" from alphavantage")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey={api_key}&outputsize=full'

    data = requests.get(url).json()
    print("data received successfully")
    return data

def get_data_from_alphavintage_compact(symbol, interval, api_key):
    print(f"requesting symbol \"{symbol}\" from alphavantage")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey={api_key}&outputsize=compact'

    data = requests.get(url).json()
    print("data received successfully")
    return data

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
