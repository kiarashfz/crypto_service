from binance import Client
from django import forms


class CryptoPriceChooserForm(forms.Form):
    PAIRED_CRYPTOS_CHOICES = []
    client = Client()
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        PAIRED_CRYPTOS_CHOICES.append((s['symbol'], s['symbol']))

    symbol = forms.ChoiceField(choices=PAIRED_CRYPTOS_CHOICES)
    price = forms.IntegerField(min_value=0)
