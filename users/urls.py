from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('me/', views.UserDetails.as_view(), name='user-details'),
    path('send-email-confirmation/',
         views.SendEmailConfirmationTokenAPIView.as_view(), name='send-email-confirmation'),
    path('confirm-email/', views.confirm_email_view, name='confirm-email')
]
