from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Project
from projects.serializers import ProjectSerializer

class TeamProjectManagement(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request: Request, project_id):
        project = Project.objects.filter(id=project_id)
        if not project.teams.members(filter=request.user).exists():
            if project.private:
                raise PermissionDenied("Only members of the team can see this private project")
        # Create serializer
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
