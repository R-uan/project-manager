from django.urls import path

from teams.views import TeamViewSet
from rest_framework.routers import DefaultRouter

team_create = TeamViewSet.as_view({"post": "create"})
team_management = TeamViewSet.as_view({"get": "retrieve", "delete": "destroy"})

urlpatterns = [
    path("", team_create, name="post_team"),
    path("<int:pk>", team_management, name="team_management"),
]
