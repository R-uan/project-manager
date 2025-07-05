from django.urls import path
from .views import MyTeams, OwnedTeams, TeamManagement

urlpatterns = [
    path('', MyTeams.as_view(), name='my_teams'),
    path('owned', OwnedTeams.as_view(), name='owned_teams'),
    path('<int:team_id>', TeamManagement.as_view(), name='membership_management')
]