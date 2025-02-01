from django.db import models
choice=(('Not Available','Not Available'),('Available','Available'))

class VoterReg(models.Model):
    fullname = models.CharField(max_length=100)
    contact = models.IntegerField()
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)  # Field to track verification status

    def __str__(self):
        return self.fullname
    
class ElectionOfficerReg(models.Model):
    id_no=models.IntegerField()
    fullname=models.CharField(max_length=20)
    contact=models.IntegerField()
    email=models.EmailField()
    address=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    
class Election(models.Model):
    election_officer = models.ForeignKey(ElectionOfficerReg, on_delete=models.CASCADE, related_name='elections')
    election_no = models.IntegerField(unique=True)
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
    
class Vote(models.Model):
    voter = models.ForeignKey(VoterReg, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class EligibleVoter(models.Model):
    election = models.ForeignKey(Election, related_name='eligible_voters', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.phone_number} - {self.election.name}'
    
class ElectionManager(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password manually if needed

    def __str__(self):
        return self.fullname
    
class PresidingOfficer(models.Model):
    officer_id = models.CharField(max_length=20, unique=True)  # Unique Officer ID
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store password as plain text (not recommended for production)

    def __str__(self):
        return self.fullname




