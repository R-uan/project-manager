from django.urls import path
from .views import TeamOwnershipManagementView, TeamView, TeamProjectsManager

urlpatterns = [
    path('', TeamView.as_view(), name='team_management'),
    path('<int:team_id>', TeamView.as_view(), name='team_management_id'),
    path('owned', TeamOwnershipManagementView.as_view(), name='owned_team_management'),
    path('projects/<int:team_id>', TeamProjectsManager.as_view(), name='team_projects'),
    path('projects/<int:team_id>/<int:project_id>', TeamProjectsManager.as_view(), name='team_projects_id'),
    path('owned/<int:team_id>', TeamOwnershipManagementView.as_view(), name='owned_team_management_id')
]
