from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    github = models.CharField(max_length=50, blank=True, null=True)