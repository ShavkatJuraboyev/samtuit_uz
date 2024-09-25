from django.urls import path
from samtuit.views.views import home, news, new

urlpatterns = [
    path('', home, name="home"),
    path('news/', news, name="news"),
    path('new/', new, name="new")
]