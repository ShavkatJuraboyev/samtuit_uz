from django.urls import path
from interaktiv.views import (
    student, login, callback,logout, 
    get_user, profile, location, education, user_application,
    grant_application_list, admins, application_detail, export_applications_excel,
    update_grant_file, re_application, re_application_admin
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
    path('update-file/<int:pk>/', update_grant_file, name='update_grant_file'),
    path('re-application/', re_application, name='re_application'),
    
    path('admins/', admins, name='admins'),
    path('application-list/<int:application_id>/', application_detail, name='application_detail'),
    path('re-application-admin/', re_application_admin, name='re_application_admin'),
    path('application-list/export-excel/', export_applications_excel, name='export_applications_excel'),


]
