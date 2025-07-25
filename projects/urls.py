from django.urls import path

from projects.views import ProjectManagerView, ProjectAssigneesView

urlpatterns = [
    path("", ProjectManagerView.as_view({"post": "new_project"}), name="projects"),
    path("<int:project_pk>", ProjectManagerView.as_view({"get": "get_project", "delete": "delete_project", "put": "update_project"}), name="projects_id"),

    path("<int:project_pk>/assignees", ProjectAssigneesView.as_view({"get": "find", "post": "add", "delete": "remove"}), name="assignees")
]
