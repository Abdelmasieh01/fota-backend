from django.db import models
import datetime

from users.models import CustomUser as User

YEAR_CHOICES = []
for r in range(2020, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


def photo_path(instance, filename):
    return "cars/{name}/{year}/{filename}".format(name=instance.name, year=instance.year, filename=filename)


class CarModelManager(models.Manager):
    def get_model(self, full_model: str):
        [name, year] = full_model.split(maxsplit=1)
        return self.get(name=name, year=year)


class CarModel(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField(choices=YEAR_CHOICES)
    picture = models.ImageField(upload_to=photo_path, blank=True)

    objects = CarModelManager()

    @property
    def full_model(self):
        return "{name} {year}".format(name=self.name, year=self.year)

    def __str__(self):
        return "{name} {year}".format(name=self.name, year=self.year)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'], name="unique_name_year")
        ]


class Car(models.Model):
    # serial = models.AutoField(primary_key=False)
    model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="cars")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cars")
    installed_firmware = models.ForeignKey(
        'main.Firmware', on_delete=models.CASCADE, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    @property
    def full_model(self):
        return self.model.full_model

    def __str__(self):
        return "{owner}'s car - Model: {model}".format(model=self.full_model, owner=self.owner.get_full_name())


class CarReport(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="reports")
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return "Report for: {owner}'s {model} car".format(owner=self.car.owner.get_full_name(), model=self.car.full_model)
