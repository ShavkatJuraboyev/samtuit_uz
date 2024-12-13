from django.urls import path
from news.views import news, new, share_post, elonlar, seminarlar, davra_suhbatlar, matbuat_anjumanlar, meetings, uchrashuvlar

urlpatterns = [
    path('', news, name="news"),
    path('new/<int:pk>/', new, name="new"),
    path('share-post/<int:pk>/', share_post, name='share_post'),

    path('announcements/', elonlar, name="elonlar"),


    path('seminars/', seminarlar, name="seminarlar"),


    path('seminars/', davra_suhbatlar, name="davra_suhbatlar"),


    path('round/talks/', matbuat_anjumanlar, name="matbuat_anjumanlar"),


    path('meetings/', meetings, name="meetings"),


    path('gatherings/', uchrashuvlar, name="uchrashuvlar"),

]
