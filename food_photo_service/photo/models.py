from django.db import models

# Create your models here.
from django.db import models


# class Food(models.Model):
#     name = models.CharField(max_length=100)
#     calories = models.IntegerField()
#     image = models.ImageField(upload_to="food_photos/")

from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Photo {self.id}"
    

class PhotoMetadata(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()


