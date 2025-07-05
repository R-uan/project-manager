from teams.models import Team, TeamMembership
from rest_framework import serializers

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = '__all__'

class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    private = serializers.BooleanField(default=True)