from django.urls import path
from samtuit.views import home, set_language, contact

urlpatterns = [
    path('', home, name="home"),
    path('set-language/', set_language, name='set_language'),
    path('contact/', contact, name='contact'),
    
]
