from rest_framework import serializers
from .models import Car, CarModel, CarClass, CarColor


class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarColor
        fields = ('name', 'hex_code')


class CarClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarClass
        fields = ('name',)


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'name', 'year', 'picture',)


class CarModelDetailsSerializer(serializers.ModelSerializer):
    available_colors = CarColorSerializer(many=True, read_only=True)
    classes = CarClassSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = ('id', 'name', 'year', 'picture', 'horsepower',
                  'available_colors', 'classes', 'total_weight_kg',
                  'max_speed_km',
                  )


class CarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(read_only=True)
    car_color = serializers.ReadOnlyField(source='car_color.name')
    car_color_code = serializers.ReadOnlyField(source='car_color.hex_code')
    car_class = serializers.ReadOnlyField(source='car_class.name')

    class Meta:
        model = Car
        fields = ('id', 'car_color', 'car_color_code', 'car_class', 'model',
                  'registration_date', 'installed_firmware')
