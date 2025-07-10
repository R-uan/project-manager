from django.urls import path

from teams.views import TeamManagementView, get_team, post_team

urlpatterns = [
    path('', post_team, name="post_team"),
    path('<int:team_id>', get_team, name="get_team"),   
    path('<int:team_id>', TeamManagementView.as_view(), name="team_management") # delete, put
]
