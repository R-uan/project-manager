from django.db import models
from accounts.models import User

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_organizations"
    )
    created_at = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)
    website = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    objects = models.Manager()


class OrganizationMember(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="members"
    )
    member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(
        choices=[("admin", "Admin"), ("member", "Member"), ("owner", "Owner")],
        default="member",
    )
    joined_at = models.DateField(auto_now_add=True)
    teams = models.ManyToManyField(
        "teams.Team", through="teams.TeamMembership", related_name="members"
    )

    objects = models.Manager()
