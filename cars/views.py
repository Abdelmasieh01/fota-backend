from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CarModel, Car
from .serializers import CarSerializer, CarModelSerializer, CarModelDetailsSerializer


class CarModelsListView(ListAPIView):
    """
    Returns a list of all car models.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelDetailsSerializer


class OnwerCarsListView(ListAPIView):
    """
    Returns the list of cars of the owner(user).
    """
    serializer_class = CarSerializer
    
    def get_queryset(self):
        queryset = self.request.user.cars
        return queryset


class SpecificCarView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        return self.request.user.cars
    

class SpecificCarModelView(RetrieveAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelDetailsSerializer
    