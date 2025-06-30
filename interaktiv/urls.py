from django.urls import path
from interaktiv.views import (
    student, login, callback,logout, 
    get_user, profile, location, education, user_application,
    grant_application_list
    )
 
urlpatterns = [
    path('student/', student, name='student'),
    path('login/', login, name='login_oauth'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('user-status/', get_user, name='get_user'),
    path('profile/', profile, name='profile'),
    path('location/', location, name='location'),   
    path('education/', education, name='education'),
    path('user-application/', user_application, name='user_application'),
    path('grant-arizalar/', grant_application_list, name='grant_application_list'),
]
