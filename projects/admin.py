from django.contrib import admin
from .models import Project, ProjectTask, TaskAssignment

# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectTask)
admin.site.register(TaskAssignment)