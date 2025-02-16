from django.db import models
choice=(('Not Available','Not Available'),('Available','Available'))

# class VoterReg(models.Model):
#     voter_id = models.CharField(max_length=100)
#     profile_picture = models.ImageField(upload_to='voters/', null=True, blank=True)
#     fullname = models.CharField(max_length=100)
#     contact = models.IntegerField()
#     email = models.EmailField()
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     verified = models.BooleanField(default=False)  # Field to track verification status

class VoterReg(models.Model):
    voter_id = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    verified = models.BooleanField(default=False)  # Must be verified before voting

    def __str__(self):
        return f"{self.fullname} ({self.voter_id})"
    
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
    
# class Election(models.Model):
#     election_officer = models.ForeignKey(ElectionOfficerReg, on_delete=models.CASCADE, related_name='elections')
#     election_no = models.IntegerField(unique=True)
#     name=models.CharField(max_length=20)
#     start_time=models.CharField(max_length=20)
#     end_time=models.CharField(max_length=20)
#     description=models.CharField(max_length=200)
#     status=models.CharField(max_length=20,choices=choice)

#     def __str__(self):
#         return self.name

# class Candidate(models.Model):
#     election = models.ForeignKey(Election, related_name='candidates', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     profile_picture = models.ImageField(upload_to='candidates/', null=True, blank=True)
#     description = models.TextField()
#     subname = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
    
# class Vote(models.Model):
#     voter = models.ForeignKey(VoterReg, on_delete=models.CASCADE)
#     election = models.ForeignKey(Election, on_delete=models.CASCADE)
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

class Election(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.election.name}"

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    fullname = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="candidates/", null=True, blank=True)

    def __str__(self):
        return f"{self.fullname} ({self.party}) - {self.position.name}"

# Vote Model
class Vote(models.Model):
    voter_id = models.CharField(max_length=100)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote for {self.candidate.fullname} by {self.voter_id}"

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




