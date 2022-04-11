from django.urls import re_path

from one_min_price.consumers import WSConsumer

ws_urlpatterns = [
    re_path(r'^ws/price/(?P<channel_name>[^/]+)/$', WSConsumer.as_asgi())
]
