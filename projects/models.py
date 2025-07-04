from django.db import models
from django.db.models import CASCADE

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    # Project can have many teams working on it so no specific foreign key (?)

class ProjectTask(models.Model):
    priority = models.IntegerField(default=0) # The higher, the more urgent
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    due_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=CASCADE, related_name='tasks') # gets all tasks from this project (project.tasks.all)

class TaskAssignment(models.Model):
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='assigned_members') # get all assigned tasks (projectTask.assigned_members.all)
    member = models.ForeignKey('teams.TeamMembership', on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments') # get all the tasks assigned to the member (teamMembership.assignments.all)
