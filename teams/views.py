from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Team, TeamMembership
from django.core.exceptions import ObjectDoesNotExist
from .serializers import TeamSerializer, MembershipSerializer, TeamCreateSerializer


class TeamView(APIView):
    permission_classes = []

    #   Gets one team in case a `team_id` is given, otherwise gets all teams the authenticated user is part of
    #   If a team is public, the user does not need to be authenticated to retrieve it.
    #   The user needs to be authenticated and a member of the team to retrieve a private team.
    def get(self, request: Request, team_id=None):
        if team_id is not None:
            try:
                team = Team.objects.get(id=team_id)
            except ObjectDoesNotExist:
                raise NotFound({'error': 'Team not found'})

            if team.private:
                if not request.user.is_authenticated:
                    raise NotAuthenticated({'error': 'Authentication required'})
                if not team.members.filter(user=request.user).exists():
                    raise PermissionDenied({'error': 'You are not a member of this private team'})

            serializer = TeamSerializer(team)
            return Response(serializer.data)
        else:
            if not request.user.is_authenticated:
                raise NotAuthenticated({'error': 'Authentication required'})

            teams = [membership.team for membership in request.user.memberships.all()]
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)

class TeamOwnershipManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, team_id=None):
        if team_id is not None:
            try:
                team = Team.objects.get(id=team_id)
            except ObjectDoesNotExist:
                raise NotFound({'error': 'Team not found'})

            if team.owner != request.user:
                raise PermissionDenied({'error': 'You are not the owner of this team'})

            serializer = TeamSerializer(team)
            return Response(serializer.data)
        else:
            teams = Team.objects.filter(owner=request.user)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)

    def post(self, request: Request):
        serializer = TeamCreateSerializer(data=request.data)
        if serializer.is_valid():
            team = Team.objects.create(
                private=serializer.validated_data['private'],
                name=serializer.validated_data['name'],
                owner=request.user,
            )

            TeamMembership.objects.create(
                user=request.user,
                team=team,
                role='owner'
            )

            return Response({'message': 'Team created', 'team_id': team.id})
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            raise NotFound({'error': 'Team not found'})

        if team.owner != request.user:
            raise PermissionDenied({'error': 'You are not the owner of this team'})

        team.delete()
        return Response({'message': 'Team successfully deleted'})
