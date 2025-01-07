from django.urls import path
from leadership.views import leader, rektorat

urlpatterns = [
    path('leader/', leader, name="leader"),
    path('leader/<slug:slug>/', rektorat, name="rektorat"),
]