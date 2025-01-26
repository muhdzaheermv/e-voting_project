from django.contrib import admin
from . models import VoterReg,ElectionOfficerReg,Election,Candidate,Vote


admin.site.register(VoterReg)
admin.site.register(ElectionOfficerReg)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Vote)

