from django.db import models

class VoterReg(models.Model):
    fullname=models.CharField(max_length=20)
    contact=models.IntegerField()
    email=models.EmailField()
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    
class ElectionOfficerReg(models.Model):
    id_no=models.IntegerField()
    fullname=models.CharField(max_length=20)
    contact=models.IntegerField()
    email=models.EmailField()
    address=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)