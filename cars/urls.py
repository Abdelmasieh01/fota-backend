from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.CarModelsListView.as_view(), name='car-models'),
    path("my-cars/", views.OnwerCarsListView.as_view(), name='my-cars')
]