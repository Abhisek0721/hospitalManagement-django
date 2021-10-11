from django.db import models
from django.utils.timezone import now


# Create your models here.
class SignupDoctor(models.Model):
    profilePic = models.ImageField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=6)
    password = models.JSONField(max_length=300) # JSONField because it will be stored in encripted form
    pincode = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return self.username


class SignupPatient(models.Model):
    profilePic = models.ImageField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    gender = models.CharField(max_length=6)
    password = models.JSONField(max_length=300) # JSONField because it will be stored in encripted form
    pincode = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return self.username
