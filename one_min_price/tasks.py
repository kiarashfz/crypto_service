from asgiref.sync import async_to_sync
from celery import shared_task
from binance import Client
from datetime import datetime

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@shared_task
def up_down(**kwargs):
    client = Client()
    last_candle = client.get_klines(symbol=kwargs['symbol'], interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)[0]
    candle_price = float(last_candle[4])
    candle_timestamp = datetime.fromtimestamp(float(last_candle[0]) / 1000)
    if candle_price > kwargs['price']:
        async_to_sync(channel_layer.group_send)(kwargs['channel_group_name'], {'type': 'channel_message',
                                                                               'message': {
                                                                                   'timestamp': str(candle_timestamp),
                                                                                   'input_price': kwargs['price'],
                                                                                   'close_price': candle_price,
                                                                                   'status': 'Up'}})
    else:
        async_to_sync(channel_layer.group_send)(kwargs['channel_group_name'], {'type': 'channel_message',
                                                                               'message': {
                                                                                   'timestamp': str(candle_timestamp),
                                                                                   'input_price': kwargs['price'],
                                                                                   'close_price': candle_price,
                                                                                   'status': 'Down'}})
