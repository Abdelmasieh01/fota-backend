from django.db import models
from django.core import validators
import datetime

from users.models import CustomUser as User

YEAR_CHOICES = []
for r in range(2020, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))

COLOR_CHOICES = [
    ('#000000', 'Black'),
    ('#FFFFFF', 'White'),
    ('#FF0000', 'Red'),
    ('#00FF00', 'Green'),
    ('#0000FF', 'Blue'),
    ('#FFFF00', 'Yellow'),
    ('#FF00FF', 'Violet'),
    ('#00FFFF', 'Cyan'),
]

CAR_CLASS_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
]


def photo_path(instance, filename):
    return "cars/{name}/{year}/{filename}".format(name=instance.name, year=instance.year, filename=filename)


class CarModelManager(models.Manager):
    def get_model(self, full_model: str):
        model_arr = full_model.split()
        name = " ".join(model_arr[:-1])
        year = model_arr[-1]
        return self.get(name=name, year=year)


class CarColor(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class CarClass(models.Model):
    name = models.CharField(max_length=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Car classes'

class CarModel(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField(choices=YEAR_CHOICES)
    picture = models.ImageField(upload_to=photo_path, blank=True)
    horsepower = models.PositiveSmallIntegerField(default=100, validators=[
        validators.MinValueValidator(100),
        validators.MaxValueValidator(1000)
    ])
    total_weight_kg = models.PositiveSmallIntegerField(default=100)
    max_speed_km = models.PositiveSmallIntegerField(default=100)
    available_colors = models.ManyToManyField(CarColor, blank=True)
    classes = models.ManyToManyField(CarClass, blank=True)

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
        User, on_delete=models.CASCADE, related_name="cars"
    )
    installed_firmware = models.ForeignKey(
        'main.Firmware', on_delete=models.CASCADE, null=True, blank=True
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    car_color = models.ForeignKey(
        CarColor, on_delete=models.CASCADE, blank=True, null=True)
    car_class = models.ForeignKey(
        CarClass, on_delete=models.CASCADE, blank=True, null=True)

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
