from rest_framework.generics import ListAPIView
from .models import CarModel, Car
from .serializers import CarSerializer, CarModelSerializer

# Create your views here.
class CarModelsListView(ListAPIView):
    """
    Returns a list of all car models.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

class OnwerCarsListView(ListAPIView):
    """
    Returns the list of cars of the owner(user).
    """
    serializer_class = CarSerializer
    
    def get_queryset(self):
        queryset = self.request.user.cars
        return queryset
