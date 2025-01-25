from django.db import models

class Voter(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    phonenumber = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class ElectionOfficer(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    id_number = models.CharField(max_length=20, unique=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    phonenumber = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username