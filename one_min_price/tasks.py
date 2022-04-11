from celery import shared_task
from binance import Client
from datetime import datetime


@shared_task
def up_down(symbol: str, price: float):
    client = Client()
    last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)[0]
    candle_price = float(last_candle[4])
    candle_timestamp = datetime.fromtimestamp(float(last_candle[0]) / 1000)
    if candle_price > price:
        return {'timestamp': candle_timestamp, 'input_price': price, 'close_price': candle_price, 'status': 'Up'}
    else:
        return {'timestamp': candle_timestamp, 'input_price': price, 'close_price': candle_price, 'status': 'Down'}
