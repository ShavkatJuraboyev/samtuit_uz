from django.urls import path
from samtuit.views import home, set_language, get_objects, get_models

urlpatterns = [
    path('', home, name="home"),
    path('set-language/', set_language, name='set_language'),
    path('admin/get_models/', get_models, name='get_models'),
    path('admin/get_objects/', get_objects, name='get_objects'),
]
