from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user


class User(AbstractUser):
    github = models.CharField(max_length=50, blank=True, null=True)
    objects = CustomUserManager()
    organizations = models.ManyToManyField(
        "organizations.Organization", through="organizations.OrganizationMember"
    )
