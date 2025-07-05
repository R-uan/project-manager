from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Team, TeamMembership
from django.core.exceptions import ObjectDoesNotExist
from .serializers import TeamSerializer, MembershipSerializer, TeamCreateSerializer


class TeamManagement(APIView):
    permission_classes = []

    def get(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Team not found'}, status=404)

        if team.private:
            if not request.user or not request.user.is_authenticated:
                return Response({'error': 'Authentication required for private team'}, status=401)
            if not team.members.filter(user=request.user).exists():
                return Response({'error': 'You are not a member of this team.'}, status=403)

        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def delete(self, request: Request, team_id):
        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required for this request'}, status=401)

        try:
            team = Team.objects.get(id=team_id, owner=request.user)
        except ObjectDoesNotExist:
            return Response({'error': 'Team not found'}, status=404)

        # if not team.owner != request.user:
        #     raise PermissionDenied("You do not own this team.")

        team.delete()
        return Response({ 'message': 'Team was successfully deleted' }, status=200)

class OwnedTeams(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request: Request):
        teams = Team.objects.filter(owner=request.user).all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class MyTeams(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        teams = TeamMembership.objects.filter(user=request.user)
        serializer = MembershipSerializer(teams, many=True)
        return Response(serializer.data)
