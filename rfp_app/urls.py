
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('scrape', views.scrape, name='scrape'),
    path('home', views.index, name='home'),
    path('sendAdaptiveCards', views.send_adaptive_cards, name='sendAdaptiveCards'),
]
