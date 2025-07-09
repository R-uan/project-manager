from django.db import models
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project

# Create your models here.


# Organizations can have many teams, but a team can only be part of an organization
class Team(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="teams"
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    projects = models.ManyToManyField(
        "projects.Project", through="teams.TeamProject", related_name="teams"
    )

    objects = models.Manager()


# Organization members can be part of many teams
class TeamMembership(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="member_teams"
    )  # get all members from this team
    member = models.ForeignKey(
        OrganizationMember, on_delete=models.CASCADE, related_name="team_members"
    )  # get all memberships from this user


# This is a relation table that links multiple projects to multiple teams and vice-versa
class TeamProject(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="projects"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="teams")
