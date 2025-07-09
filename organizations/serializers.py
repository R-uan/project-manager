from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationCreationRequest(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    private = serializers.BooleanField(default=False)
    website = serializers.CharField(max_length=100, default="")
    linkedin = serializers.CharField(max_length=100, default="")
    email = serializers.EmailField(max_length=254, default="")
