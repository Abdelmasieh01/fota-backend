from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('models/', views.CarModelsListView.as_view(), name='car-models'),
    path('models/<int:pk>', views.SpecificCarModelView.as_view(), name='car-model'),
    path("my-cars/", views.OnwerCarsListView.as_view(), name='my-cars'),
    path('my-cars/<int:pk>', views.SpecificCarView.as_view(), name='car-model'),
]