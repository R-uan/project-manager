from django.contrib import admin
from .models import Team, TeamMembership, TeamProject

# Register your models here.

admin.site.register(Team)
admin.site.register(TeamProject)
admin.site.register(TeamMembership)
