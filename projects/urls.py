from django.urls import path

from projects.views import ProjectManagerView

urlpatterns = [
    path("", ProjectManagerView.as_view({"post": "new_project"}), name="projects"),
    path("<int:project_pk>", ProjectManagerView.as_view({"get": "get_project", "delete": "delete_project", "put": "update_project"}), name="projects_id")
]
