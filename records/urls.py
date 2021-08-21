from django.urls import path
from . import views
from .views import(
    AlumniDetailView,
    AlumniUpdateViewGate,
    AlumniUpdateView,
    alumni_login,
    alumni_logged_in,
    record_home,
    YearbookListView,
)
from .admin_view import send_email_admin

urlpatterns =[
    path('', record_home, name='record-home'),
    path('login/', alumni_login, name='alumni-login'),
    path('accounts/profile/', alumni_logged_in, name='alumni-logged-in'),
    # path('<batch_bs>/<program_code>/<roll_number>/', AlumniDetailView.as_view(), name='record-detail'),
    path('<batch_bs>/<program_code>/yearbook/', YearbookListView.as_view(), name='yearbook-view'),
    path('<batch_bs>/<program_code>/<roll_number>/<last_name>/<dob_bs>/update/', AlumniUpdateViewGate, name='record-update-gate'),
    path('<batch_bs>/<program_code>/<roll_number>/<last_name>/<dob_bs>/update/', AlumniUpdateView.as_view(), name='record-update'),
    path('admin/records/student/email_send',send_email_admin,name='email-form'),
]
