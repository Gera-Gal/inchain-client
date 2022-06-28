from django.urls import path

from . import views

app_name = 'cryptos'
urlpatterns = [
    path('charts', views.crypto_charts, name='crypto_charts'),
    path('browser', views.crypto_browser, name='crypto_browser'),
    path('_get_listing', views.get_listing, name='get_listing'),
]