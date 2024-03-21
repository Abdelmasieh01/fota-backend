from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.UserDetails.as_view(), name='user-details'),
]