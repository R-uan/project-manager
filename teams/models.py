from django.db import models
from accounts.models import User


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')  # get all teams this user owns
    projects = models.ManyToManyField('projects.Project', through='projects.ProjectTeam', related_name='teams')
    objects = models.Manager()


class TeamMembership(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')  # get all members from this team
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')  # get all memberships from this user
    role = models.CharField(choices=[('admin', 'Admin'), ('member', 'Member'), ('owner', 'Owner')], default='member')
    objects = models.Manager()

class TeamProject(models.Model):
    is_archives = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='shared_projects')  # gets all projects from this team
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='collaborating_teams')  # gets all teams working on this project
    objects = models.Manager()
