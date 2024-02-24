from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Firmware, FirmwareLine
from .serializers import FirmwareSerializer, FirmwareLineSerializer
from cars.models import Car, CarModel

# Create your views here.
@api_view(['GET'])
def ping(request):
    return Response(data={'status': 'ok'}, status=status.HTTP_200_OK)


class FirmwareListView(ListAPIView):
    """
    Queries for firmwares using car model or car model year or get all firmwares.
    """
    serializer_class = FirmwareSerializer

    def get_queryset(self):
        queryset = Firmware.objects.all()
        car_model_name = self.request.query_params.get("model")
        year = self.request.query_params.get("year")
        if car_model_name or year:
            car_models = CarModel.objects.all()
            if car_model_name:
                car_models = car_models.filter(name=car_model_name)
            if year:
                car_models = car_models.filter(year=int(year))
            queryset.filter(car_model__in=car_models)
        return queryset


class FirmwareLineListView(ListAPIView):
    """
    Retunrs a list of FirmwareLine objects that are related to certain firmware.
    """
    serializer_class = FirmwareLineSerializer

    def get_queryset(self):
        queryset = FirmwareLine.objects.all()
        firmware_version = self.request.query_params.get("version")
        firmware_model = self.request.query_params.get("full_model")
        if not firmware_model or firmware_version:
            return queryset.none()
        
        model = CarModel.objects.get_model(firmware_model)
        return queryset.filter(model=model, queryset=queryset)


@api_view(['GET'])
def get_latest_car_firmware(request, car_id):
    """
    Gets the latest firmware of a car using the car id.
    """
    try:
        car = Car.objects.select_related('model').get(pk=car_id)
        firmware = Firmware.objects.get_latest(model=car.model)
        if not firmware:
            raise ObjectDoesNotExist
        
        item = FirmwareSerializer(firmware)
    except ObjectDoesNotExist:
        return Response(data={"message": "Firmware or car model not found!"}, status=status.HTTP_404_NOT_FOUND)

    return Response(data=item.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_latest_model_firmware(request, full_model: str):
    """
    Gets the latest firmware of a car model using the full model.
    """
    try:
        model = CarModel.objects.get_model(full_model)
        firmware = Firmware.objects.get_latest(model=model)
        if not firmware:
            raise ObjectDoesNotExist
        item = FirmwareSerializer(firmware)
    except ObjectDoesNotExist:
        return Response(data={"message": "Firmware or Model Could not be found!"}, status=status.HTTP_404_NOT_FOUND)

    return Response(data=item.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_firmware_line(request, firmware_id, number):
    """
    Gets a single firmware line object.
    """
    try:
        firmware = Firmware.objects.get(pk=firmware_id)
        line = FirmwareLine.objects.get(firmware=firmware, number=number)
        item = FirmwareLineSerializer(line)
    except ObjectDoesNotExist:
        return Response(data={"message": "Firmware or FirmwareLine Could not be found!"}, status=status.HTTP_404_NOT_FOUND)

    return Response(data=item.data, status=status.HTTP_200_OK)

        

        