from crypto_service.service import paired_cryptos_cache_checker
from django_redis import get_redis_connection
from django import forms

cache = get_redis_connection('default')
paired_cryptos_cache_checker()


class CryptoPriceChooserForm(forms.Form):
    symbol = forms.ChoiceField(choices=[tuple(str(pair.decode("utf-8")).split(",")) for pair in
                                        cache.lrange('CS_PAIRED_CRYPTOS_CHOICES', 0, -1)])
    price = forms.IntegerField(min_value=0)
    channel_name = forms.CharField(max_length=100)
