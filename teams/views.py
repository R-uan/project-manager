from django.db.models import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.response import Response
from .models import Team, Organization
from .serializers import TeamSerializer, TeamCreateSerializer


class TeamViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = TeamCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        organization_id = serializer.validated_data["organization_id"]

        try:
            organization = Organization.objects.get(id=organization_id)
        except ObjectDoesNotExist:
            raise NotFound("Organization does not exist")

        membership = organization.members.filter(member=request.user).first()
        if not membership or membership.role not in ["admin", "owner"]:
            raise PermissionDenied("You're not allowed to create a team")

        team = Team.objects.create(
            organization=organization,
            name=serializer.validated_data["name"],
        )

        return Response(
            {"message": "Team created", "teamId": team.id},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        try:
            team = Team.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound("Team does not exist")

        if team.organization.private:
            if not request.user.is_authenticated:
                raise NotAuthenticated("Authentication needed")
            if not request.user.organizations.filter(id=team.organization.id).exists():
                raise PermissionDenied("You're not part of this organization")

        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("Authentication needed")

        try:
            team = Team.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound("Team does not exist")

        membership = team.members.filter(member=request.user).first()
        if not membership or membership.role not in ["admin", "owner"]:
            raise PermissionDenied("You do not have permission to do this")

        team.delete()
        return Response(
            {"message": "Team successfully deleted"}, status=status.HTTP_204_NO_CONTENT
        )
