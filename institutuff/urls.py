from django.urls import path
from . import views

urlpatterns =[
    #path('', record_home, name='record-home'),
    path('inst_login/', views.institute_login, name='institute-log-in'),
    path('inst_logout/', views.logout_institute, name='institute-log-out'),
    path('institute/', views.institute_logged_in, name='institute-logged-in'),
    path('institute/view',views.view_alumni.as_view(), name='view-alumni'),
]
