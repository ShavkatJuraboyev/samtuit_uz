from django.urls import path
from news.views.views import (
        news, new, share_post, elonlar, seminarlar, davra_suhbatlar, 
        matbuat_anjumanlar, meetings, uchrashuvlar, detail
    )
from news.views.home import (
        menu_view, view_menu_detail
    )

urlpatterns = [
    path('news/', news, name="news"), 
    path('new/<int:pk>/', new, name="new"),
    path('share-post/<int:pk>/', share_post, name='share_post'),

    path('announcements/', elonlar, name="elonlar"),


    path('seminars/', seminarlar, name="seminarlar"),


    path('seminar/', davra_suhbatlar, name="davra_suhbatlar"),


    path('round/talks/', matbuat_anjumanlar, name="matbuat_anjumanlar"),


    path('meetings/', meetings, name="meetings"),


    path('gatherings/', uchrashuvlar, name="uchrashuvlar"),

    path('about/<slug:slug>/', detail, name='detail'),

    path('<slug:slug>/', menu_view, name='menu_view'),
    path('detail/<int:pk>/', view_menu_detail, name='view_menu_detail'),

]
