from django.urls import path
from samtuit.views.views import home, news, new, share_post, elonlar, seminarlar, set_language
from samtuit.views.meetings import davra_suhbatlar, matbuat_anjumanlar, meetings, uchrashuvlar

urlpatterns = [
    path('', home, name="home"),
    path('set-language/', set_language, name='set_language'),

    path('news/', news, name="news"),
    path('news/<int:pk>/new', new, name="new"),
    path('share-post/<int:pk>/', share_post, name='share_post'),

    path('announcements/', elonlar, name="elonlar"),


    path('seminars/', seminarlar, name="seminarlar"),


    path('seminars/', davra_suhbatlar, name="davra_suhbatlar"),


    path('round/talks/', matbuat_anjumanlar, name="matbuat_anjumanlar"),


    path('meetings/', meetings, name="meetings"),


    path('gatherings/', uchrashuvlar, name="uchrashuvlar"),

]