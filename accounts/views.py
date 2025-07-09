from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from organizations.serializers import OrganizationSerializer
from .serializers import AccountCreationSerializer
from .models import User

# Create your views here.


class AccountManagement(APIView):
    def post(self, request: Request):
        serializer = AccountCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            github=serializer.validated_data["github"],
        )
        return Response(user.username, status=200)

    def put(self, request: Request):
        if not request.user or request.user.is_authenticated:
            return Response("{ error: 'You need to be authenticated' }", status=401)

        user = request.user
        data = request.data

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "github" in data:
            user.github = data["github"]
        if "email" in data:
            user.email = data["email"]

        user.save()
        return Response('{ message: "User successfully updated" }', status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_organizations(request: Request, organization_id=None):
    if not organization_id:
        organizations = request.user.organizations.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    try:
        organization = request.user.organizations.get(id=organization_id)
    except ObjectDoesNotExist:
        raise NotFound({"error": "Organization not found"})

    serializer = OrganizationSerializer(organization)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_owned_organizations(request: Request, organization_id=None):
    if not organization_id:
        organizations = request.user.owned_organizations.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    try:
        organization = request.user.owned_organizations.get(id=organization_id)
    except ObjectDoesNotExist:
        raise NotFound({"error": "Organization not found"})

    serializer = OrganizationSerializer(organization)
    return Response(serializer.data)
