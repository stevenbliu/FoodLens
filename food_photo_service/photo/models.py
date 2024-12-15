from django.db import models

# Create your models here.
from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    image = models.ImageField(upload_to="food_photos/")
