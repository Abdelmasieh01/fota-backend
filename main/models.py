from django.db import models

# Create your models here.


class Firmware(models.Model):
    name = models.CharField(max_length=50)
    version = models.CharField(unique=True, max_length=10)
    file = models.FileField()

    def __str__(self):
        return 'Firmware: ' + self.name + ' - ' + 'Version: ' + self.version
