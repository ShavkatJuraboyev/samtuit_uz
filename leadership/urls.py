from django.urls import path
from leadership.views import leader, rektorat, kafedralar, kafedra, markaz, markazlar, fakultetlar, fakultet, dekan

urlpatterns = [
    path('leader/', leader, name="leader"),
    path('leader/<slug:slug>/', rektorat, name="rektorat"),

    path('kafedralar/', kafedralar, name="kafedralar"),
    path('kafedra/<slug:slug>/', kafedra, name="kafedra"),

    path('markazlar/', markazlar, name="markazlar"),
    path('markaz/<slug:slug>/', markaz, name="markaz"),

    path('fakultetlar/', fakultetlar, name="fakultetlar"),
    path('fakultet/<slug:slug>/', fakultet, name="fakultet"),
    path('dekan/<slug:slug>/', dekan, name="dekanl"),


]