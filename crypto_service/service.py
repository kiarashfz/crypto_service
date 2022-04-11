from binance import Client
from django_redis import get_redis_connection

cache = get_redis_connection('default')


def paired_cryptos_cache_checker():
    status = cache.get('CS_PAIRED_STATUS')
    if not status:
        client = Client()
        exchange_info = client.get_exchange_info()
        [cache.rpush('CS_PAIRED_CRYPTOS_CHOICES', f"{s['symbol']},{s['symbol']}") for s in exchange_info['symbols']]
        cache.set('CS_PAIRED_STATUS', 1)
