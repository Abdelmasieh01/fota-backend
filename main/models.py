from django.db import models
from cars.models import Car
# Create your models here.

def file_path(instance, filename):
    return f'firmwares/{instance.name}/{filename}'


class Firmware(models.Model):
    version = models.CharField(max_length=10)
    file = models.FileField(upload_to=file_path)
    car_model = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="firmwares")

    @property
    def full_model(self):
        return self.car_model.full_model()        

    def __str__(self):
        return self.name + ' - ' + 'Version: ' + self.version
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['version', 'car_model'], name='unique_version_car_model')
        ]


class FirmwareLine(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    line = models.CharField(max_length=200)

    @property
    def firmware_name(self):
        return self.firmware.name
    
    @property
    def firmware_car(self):
        return self.firmware.car_model

    def __str__(self):
        return f'Line Number: {self.number} of firmware: {self.firmware_name}'
