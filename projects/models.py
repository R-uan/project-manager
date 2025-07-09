from django.db import models
from django.db.models import CASCADE
from organizations.models import Organization
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ProjectStatus(models.IntegerChoices):
    ONGOING = 0, _("Ongoing")
    COMPLETED = 1, _("Completed")
    PAUSED = 2, _("Paused")
    CANCELLED = 3, _("Cancelled")


# Organizations can have many projects, a project can belong to only one organization
class Project(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=ProjectStatus.choices, default=ProjectStatus.ONGOING
    )
    private = models.BooleanField(default=False)
    secret = models.BooleanField(default=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects"
    )

    objects = models.Manager()


# A project can have many tasks, a task can only belong to one project
class ProjectTask(models.Model):
    priority = models.IntegerField(default=0)  # The higher, the more urgent
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    due_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=CASCADE, related_name="tasks"
    )  # gets all tasks from this project (project.tasks.all)

    objects = models.Manager()


# A member can be assigned many tasks, a task can belong to many members
class TaskAssignment(models.Model):
    task = models.ForeignKey(
        ProjectTask, on_delete=models.CASCADE, related_name="assigned_members"
    )  # get all assigned tasks (projectTask.assigned_members.all)
    member = models.ForeignKey(
        "teams.TeamMembership",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments",
    )  # get all the tasks assigned to the member (teamMembership.assignments.all)
