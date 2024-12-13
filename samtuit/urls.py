from django.urls import path
from samtuit.views.views import home, set_language

urlpatterns = [
    path('', home, name="home"),
    path('set-language/', set_language, name='set_language'),
]
