from django.db import models
from accounts.models import User


# Create your models here.


class Organization(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_organizations")

    created_at = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)

    website = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)


class OrganizationMember(models.Model):
    objects = models.Manager()

    joined_at = models.DateField(auto_now_add=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organizations")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(choices=[("admin", "Admin"), ("member", "Member"), ("owner", "Owner")], default="member")
    tasks = models.ManyToManyField("projects.ProjectTask", through="projects.TaskAssignment", related_name="assignees")
