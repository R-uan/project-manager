from rest_framework import serializers

from accounts.models import User


class AccountCreationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    github = serializers.CharField(max_length=50, default="")

class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
