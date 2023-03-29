from django.db import models

# Create your models here.

# User Model
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.JSONField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)




