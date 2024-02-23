from django.shortcuts import render
from rest_framework.generics.views import ListAPIView
from .models import CarModel, Car
from .serializers import CarSerializer

# Create your views here.
class CarModelsListView(ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
