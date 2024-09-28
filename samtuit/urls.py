from django.urls import path
from samtuit.views.views import home, news, new, share_post

urlpatterns = [
    path('', home, name="home"),
    path('news/', news, name="news"),
    path('news/<int:pk>/new', new, name="new"),
    path('share-post/<int:pk>/', share_post, name='share_post'),
]