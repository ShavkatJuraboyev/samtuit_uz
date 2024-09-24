from django.urls import path
from samtuit.views import home, news

urlpatterns = [
    path('', home, name="home"),
    path('news/', news, name="news")
]