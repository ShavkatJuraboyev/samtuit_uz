from django.urls import path
from news.views.views import (
        news, new, share_post, elonlar, elon, seminarlar, davra_suhbatlar, 
        matbuat_anjumanlar, meetings, meeting, uchrashuvlar, detail, uchrashuv, matbuat_anjuman, seminar, davra_suhbat
    )
from news.views.home import (
        menu_view, view_menu_detail
    )
 
urlpatterns = [
    path('news/', news, name="news"),  
    path('new/<int:pk>/', new, name="new"),
    path('share-post/<int:pk>/', share_post, name='share_post'),

    path('announcements/', elonlar, name="elonlar"),
    path('announcements/<int:pk>/', elon, name='elon'),


    path('meetings/', meetings, name="meetings"),
    path('meeting/<int:pk>/', meeting, name="meeting"),


    path('gatherings/', uchrashuvlar, name="uchrashuvlar"),
    path('gathering/<int:pk>/', uchrashuv, name="uchrashuv"),

    path('seminars/', seminarlar, name="seminarlar"),
    path('seminar/<int:pk>/', seminar, name="seminar"),


    path('conversations/', davra_suhbatlar, name="davra_suhbatlar"),
    path('conversation/<int:pk>/', davra_suhbat, name="davra_suhbat"),



    path('round/talks/', matbuat_anjumanlar, name="matbuat_anjumanlar"),
    path('round/talks/<int:pk>/', matbuat_anjuman, name="matbuat_anjuman"),

    path('about/<slug:slug>/', detail, name='detail'),

    path('<slug:slug>/', menu_view, name='menu_view'),
    path('detail/<int:pk>/', view_menu_detail, name='view_menu_detail'),
]
