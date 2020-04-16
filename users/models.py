from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class User(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=128,unique=True,null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=1024,null=True)
    phone = models.CharField(max_length=20,null=True)
    license =  models.CharField(max_length=30,null=True)
    car_make = models.CharField(max_length=30,null=True)
    car_model = models.CharField(max_length=30,null=True)
    car_year = models.IntegerField(null=True)
    car_colour = models.CharField(max_length=30,null=True)
    car_county = models.CharField(max_length=30,null=True)
    car_plate = models.CharField(max_length=30,null=True)
    time = models.DateTimeField(auto_now_add=True)
    group = models.IntegerField(null=False)
    image = models.ImageField(default='user.png', upload_to='media/', blank=True, null=True)

    def __str__(self):
        return str(self.email) if self.email else ''