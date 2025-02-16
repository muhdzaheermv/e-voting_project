from django.contrib import admin
from . models import VoterReg,ElectionOfficerReg,Election,Candidate,EligibleVoter,ElectionManager,PresidingOfficer,Position


admin.site.register(VoterReg)
admin.site.register(ElectionOfficerReg)
# admin.site.register(Election)
# admin.site.register(Candidate)
# admin.site.register(Vote)
admin.site.register(EligibleVoter)
admin.site.register(ElectionManager)
admin.site.register(PresidingOfficer)

admin.site.register(Election)
admin.site.register(Position)
admin.site.register(Candidate)

