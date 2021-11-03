from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    pass

class LineTilingHistoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    horizontal_tilt = models.FloatField()
    horizontal_interval = models.FloatField()
    vertical_tilt = models.FloatField()
    vertical_interval = models.FloatField()
    horizontal_max = models.IntegerField()
    vertical_max = models.IntegerField()

class ParabolaTilingHistoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    parabola_tilt = models.FloatField()
    horizontal_interval = models.FloatField()
    vertical_interval = models.FloatField()
    horizontal_max = models.IntegerField()
    vertical_max = models.IntegerField()

class WaveTilingHistoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    vertical_interval = models.FloatField()
    waves_number = models.IntegerField()
    horizontal_max = models.IntegerField()
    vertical_max = models.IntegerField()
    