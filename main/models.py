from django.db import models
from cars.models import CarModel
# Create your models here.


def file_path(instance, filename):
    return f'firmwares/{instance.name}/{filename}'


class FirmwareManager(models.Manager):
    def get_latest(self, model):
        return self.filter(car_model=model).order_by("-version").last()


class Firmware(models.Model):
    version = models.CharField(max_length=5)
    file = models.FileField(upload_to=file_path)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="firmwares")
    specific = models.BooleanField(default=False)
    
    objects = FirmwareManager()

    @property
    def full_model(self) -> str:
        return self.car_model.full_model()

    def __str__(self):
        return self.full_model + ' - ' + 'Version: ' + self.version

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['version', 'car_model'], name='unique_version_car_model')
        ]


class FirmwareLine(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    line = models.CharField(max_length=200)

    @property
    def firmware_name(self):
        return self.firmware.full_model

    @property
    def firmware_car(self):
        return self.firmware.car_model

    def __str__(self):
        return f'Line Number: {self.number} of firmware: {self.firmware_name}'
