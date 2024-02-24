from rest_framework import serializers
from .models import Car, CarModel


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:    
        model = CarModel
        fields = ('name', 'year')


class CarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(read_only=True)
    class Meta:
        model = Car
        fields = ('model', 'registration_date')