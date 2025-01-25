from django.contrib import admin
from .models import Voter,ElectionOfficer

admin.site.register(Voter)

admin.site.register(ElectionOfficer)
