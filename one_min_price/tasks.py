from celery import shared_task
from binance import Client
from datetime import datetime


@shared_task
def up_down(symbol: str, price: float):
    client = Client()
    last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)[-1]
    candle_price = float(last_candle[4])
    candle_timestamp = datetime.fromtimestamp(float(last_candle[0]) / 1000)
    if candle_price > price:
        return f'time:{candle_timestamp} --- Up'
    else:
        return f'time:{candle_timestamp} --- Down'
