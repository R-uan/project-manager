from rest_framework import serializers
from .models import Organization, OrganizationMember


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="member.first_name")
    last_name = serializers.CharField(source="member.last_name")

    class Meta:
        model = OrganizationMember
        fields = ["id", "first_name", "last_name", "role", "joined_at"]


class OrganizationCreationRequest(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    private = serializers.BooleanField(default=False)
    website = serializers.CharField(max_length=100, default="", allow_null=True)
    linkedin = serializers.CharField(max_length=100, default="", allow_null=True)
    email = serializers.EmailField(max_length=254, default="", allow_null=True)

class OrganizationUpdateRequest(serializers.Serializer):
    private = serializers.BooleanField(default=None, allow_null=True)
    name = serializers.CharField(max_length=30, default=None, allow_null=True)
    website = serializers.CharField(max_length=100, default=None, allow_null=True)
    linkedin = serializers.CharField(max_length=100, default=None, allow_null=True)
    email = serializers.EmailField(max_length=254, default=None, allow_null=True)


class OrganizationAddMember(serializers.Serializer):
    member_pk = serializers.CharField()
    role = serializers.CharField(default="member", allow_null=True)
