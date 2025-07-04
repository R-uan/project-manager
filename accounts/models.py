from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    github = models.CharField(max_length=50, blank=True, null=True)