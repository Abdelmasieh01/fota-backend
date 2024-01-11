from django.db import models

# Create your models here.

def file_path(instance, filename):
    return f'firmwares/{instance.name}/{filename}'


class Firmware(models.Model):
    name = models.CharField(max_length=50)
    version = models.CharField(unique=True, max_length=10)
    file = models.FileField(upload_to=file_path)

    def __str__(self):
        return self.name + ' - ' + 'Version: ' + self.version


class FirmwareLine(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    line = models.CharField(max_length=200)

    @property
    def firmware_name(self):
        return self.firmware.name

    def __str__(self):
        return f'Line Number: {self.number} of firmware: {self.firmware_name}'
