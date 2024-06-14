from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Queue(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    report = models.ForeignKey('cars.CarReport', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() + " " + str(self.timestamp)