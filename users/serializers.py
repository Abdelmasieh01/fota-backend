from rest_framework import serializers
from .models import CustomUser
from cars.serializers import CarSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    def save(self, request):
        user = CustomUser(
            email=self.validated_data.get('email'),
            phone=self.validated_data.get('phone'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            photo=self.validated_data.get('photo'),
        )
        password1 = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        user.set_password(password1)
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'first_name', 'last_name',
                  'photo', 'password', 'password2')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'first_name', 'last_name', 'photo', 'is_customer_service')


class UserDetailsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'first_name', 'last_name', 'photo', 'cars', 'is_email_confirmed', 'is_customer_service')
