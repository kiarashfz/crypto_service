from django.urls import path
from .views import Index

app_name = 'one_min_price'
urlpatterns = [
    path('', Index.as_view(), name='index'),
]
