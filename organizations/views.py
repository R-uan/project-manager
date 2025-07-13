from django.db.models import Q, ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.request import Request
from rest_framework.views import APIView, PermissionDenied, Response
from rest_framework.decorators import api_view, permission_classes
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from organizations.serializers import (
    OrganizationAddMember,
    OrganizationCreationRequest,
    OrganizationMemberSerializer,
    OrganizationSerializer,
)

# Create your views here.
class OrganizationView(APIView):
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

                if not organization.members.get(member=request.user).exists():
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


@api_view(['GET'])
def get_organization_members(request: Request, pk):
    try:
        org = Organization.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise NotFound({'error': 'Organization was not found'})

    if not org.private:
        members = org.members.all()
        serializer = OrganizationMemberSerializer(members, many=True)
        return Response(serializer.data)        

    if not request.user.is_authenticated:
        raise NotAuthenticated("Authorization needed")

    if not org.members.filter(member=request.user).exists():
        raise PermissionDenied("You're not allowed to see this")

    members = org.members.all()
    serializer = OrganizationMemberSerializer(members, many=True)
    return Response(serializer.data)
    
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_organization_member(request: Request, pk):
    data = OrganizationAddMember(data=request.data)
    if not data.is_valid():
        return Response(data.errors, 400)
    if data.validated_data['role'] not in ['admin', 'member']:
        return Response("Invalid role assignment", 400)
        
    try:
        org = Organization.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise NotFound({'error': 'Organization was not found'})

    try:
        member = org.members.get(id=request.user.id)
    except ObjectDoesNotExist:
        raise PermissionDenied("You can't do that")

    if member.role not in ["admin", "owner"]:
        raise PermissionDenied("You can't do that")

    if data.validated_data['role'] == "admin" and member.role != 'owner':
        raise PermissionDenied("You can't assign that role")

    try:
        new_member = User.objects.get(id=data.validated_data['member_pk'])
    except ObjectDoesNotExist:
        raise NotFound("New member was not found")
    
    OrganizationMember.objects.create(
        organization=org,
        member=new_member,
        role=data.validated_data['role'],
    )

    return Response({'message': 'Member added'})
        
