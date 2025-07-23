from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class NewProjectSerializer(serializers.Serializer):
    organization = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    secret = serializers.BooleanField(default=False)
    private = serializers.BooleanField(default=True)
    status = serializers.IntegerField(default=0)


class UpdateProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, allow_null=True, default=None)
    secret = serializers.BooleanField(allow_null=True, default=None)
    private = serializers.BooleanField(allow_null=True, default=None)
    status = serializers.IntegerField(allow_null=True, default=None)


class AssignProjectMember(serializers.Serializer):
    member_pk = serializers.IntegerField()

