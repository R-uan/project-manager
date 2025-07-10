from django.db.models import Q
from rest_framework.request import Request
from rest_framework.views import APIView, PermissionDenied, Response
from organizations.models import Organization
from organizations.serializers import (
    OrganizationCreationRequest,
    OrganizationSerializer,
)


# Create your views here.
class OrganizationManagerView(APIView):
    def get(self, request: Request, organization_id=None):
        if not organization_id:
            if request.user.is_authenticated:
                organizations = Organization.objects.filter(
                    Q(private=False) | Q(members__member=request.user)
                ).distinct()
            else:
                organizations = Organization.objects.filter(private=False)

            serializer = OrganizationSerializer(organizations, many=True)
            return Response(serializer.data)
        else:
            organization = Organization.objects.get(id=organization_id)
            if organization.private:
                if not request.user.is_authenticated:
                    raise PermissionDenied({"error": "Authentication needed"})

                if not organization.members.get(member=request.uer).exists():
                    raise PermissionDenied(
                        {"error": "You can not see this private organization"}
                    )

                serializer = OrganizationSerializer(organization)
                return Response(serializer.data)

    def post(self, request: Request):
        if not request.user.is_authenticated:
            raise PermissionDenied({"error": "You need to be authenticated"})

        serializer = OrganizationCreationRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        organization = Organization.objects.create(
            name=serializer.validated_data["name"],
            owner=request.user,
            private=serializer.validated_data["private"],
            website=serializer.validated_data["website"],
            linkedin=serializer.validated_data["linkedin"],
            email=serializer.validated_data["email"],
        )

        return Response(
            {"message": "Organization created", "organizationId": organization.id}
        )
