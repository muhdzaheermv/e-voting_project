from django.db import models
choice=(('Not Available','Not Available'),('Available','Available'))

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
    
class Election(models.Model):
    election_no=models.IntegerField()
    name=models.CharField(max_length=20)
    start_time=models.CharField(max_length=20)
    end_time=models.CharField(max_length=20)
    description=models.CharField(max_length=200)
    status=models.CharField(max_length=20,choices=choice)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    election = models.ForeignKey(Election, related_name='candidates', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='candidates/', null=True, blank=True)
    description = models.TextField()
    subname = models.CharField(max_length=255)

    def __str__(self):
        return self.name

