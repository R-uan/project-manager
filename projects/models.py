from django.db import models
from django.db.models import CASCADE
from organizations.models import Organization, OrganizationMember
from django.utils.translation import gettext_lazy as _


# Create your models here.

class ProjectStatus(models.IntegerChoices):
    ONGOING = 0, _("Ongoing")
    COMPLETED = 1, _("Completed")
    PAUSED = 2, _("Paused")
    CANCELLED = 3, _("Cancelled")


# Organizations can have many projects, a project can belong to only one organization
class Project(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)
    secret = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.ONGOING)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    assignees = models.ManyToManyField("organizations.OrganizationMember", through="projects.ProjectAssignment", related_name="projects")


# A project can have many assigned members working on it, a member can be assigned to multiple projects
class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey("organizations.OrganizationMember", on_delete=models.CASCADE)


# A project can have many tasks, a task can only belong to one project
class ProjectTask(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)  # The higher, the more urgent
    created_at = models.DateTimeField(auto_created=True)
    due_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=CASCADE, related_name="tasks")  # gets all tasks from this project (project.tasks...)


# A member can be assigned many tasks, a task can belong to many members
class TaskAssignment(models.Model):
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    member = models.ForeignKey("organizations.OrganizationMember", on_delete=models.CASCADE)
