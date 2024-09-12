from django.urls import path
from samtuit.views import home

urlpatterns = [
    path('', home, name="home")
]