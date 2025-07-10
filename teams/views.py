from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from organizations.models import Organization
from projects.serializers import ProjectSerializer
from .models import Team, TeamMembership
from django.core.exceptions import ObjectDoesNotExist
from .serializers import TeamSerializer, TeamCreateSerializer
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_team(request: Request):
        validator = TeamCreateSerializer(request.data)
        if not validator.is_valid:
            return Response(validator.errors, 400)

        organization_id = validator.validated_data["organization_id"]

        try:
            organization = Organization.objects.get(organization_id)
        except ObjectDoesNotExist:
            raise NotFound("Organization does not exist")

        user_membership = organization.members.filter(member=request.user)
        if user_membership.role != "admin" or "owner":
            raise PermissionDenied("You're not allowed to create a team")

        team = Team.objects.create(
            organization=organization,
            name=validator.validated_data["name"],
        )

        return Response({"message": "Team created", "teamId": team.id})

@api_view(['GET'])
def get_team(request: Request, team_id):
        team = Team.objects.get(id=team_id)
        if team.organization.private:
            if not request.user.is_authenticated:
                raise NotAuthenticated("Authentication needed")
            try:
                request.user.organizations.get(id=team.organization.id)
            except ObjectDoesNotExist:
                raise PermissionDenied("You're not part of this organization")

        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
class TeamManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            raise NotFound("Team does not exist")
        try:
            member = team.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied("Could not find membership")

        if member.role != "admin" or " owner":
            raise PermissionDenied("You do not have permission to do this")

        team.delete()
        return Response({"message": "Team successfully deleted"})
