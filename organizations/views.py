from django.db.models import Q, ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.request import Request
from rest_framework.views import APIView, PermissionDenied, Response
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from organizations.serializers import (
    OrganizationAddMember,
    OrganizationCreationRequest,
    OrganizationMemberSerializer,
    OrganizationSerializer,
)
from projects.serializers import ProjectSerializer


# api/organizations
# api/organizations/<int:org_pk>
class OrganizationView(viewsets.ViewSet):
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
                    raise PermissionDenied({"error": "Authorization needed"})

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

    def delete(self, request: Request, org_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated({"error": "You need to be authenticated"})

        try:
            org = Organization.objects.get(id=org_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Organization was not found"})

        if org.owner != request.user:
            raise PermissionDenied({"error": "Only the owner can delete the organization"})

        org.delete()
        return Response({"message": "The organization was deleted"})

# api/organizations/<int:org_pk>/members
# api/organizations/<int:org_pk>/members/<int:member_pk>
class OrganizationMemberManagementView(viewsets.ViewSet):
    permission_classes = []

    def members(self, request: Request, org_pk):
        try:
            org = Organization.objects.get(id=org_pk)
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

    def create(self, request: Request, org_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        data = OrganizationAddMember(data=request.data)

        if not data.is_valid():
            return Response(data.errors, 400)
        if data.validated_data['role'] not in ['admin', 'member']:
            return Response({"error": "Invalid role assignment"}, 400)

        try:
            org = Organization.objects.get(id=org_pk)
        except ObjectDoesNotExist:
            raise NotFound({'error': 'Organization was not found'})

        try:
            member = org.members.get(id=request.user.id)
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You can't do that"})

        if member.role not in ["admin", "owner"]:
            raise PermissionDenied({"error": "You can't do that"})

        if data.validated_data['role'] == "admin" and member.role != 'owner':
            raise PermissionDenied({"error": "You can't assign that role"})

        try:
            new_member = User.objects.get(id=data.validated_data['member_pk'])
        except ObjectDoesNotExist:
            raise NotFound({"error": "Target member was not found"})

        OrganizationMember.objects.create(
            organization=org,
            member=new_member,
            role=data.validated_data['role'],
        )

        return Response({'message': 'Member added'})

    def destroy(self, request: Request, org_pk, member_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        try:
            org = Organization.objects.get(id=org_pk)
        except ObjectDoesNotExist:
            raise NotFound({'error': 'Organization was not found'})

        try:
            user = User.objects.get(id=member_pk)
            member = org.members.get(member=user)
        except ObjectDoesNotExist:
            raise NotFound({'error': 'Could not find target member'})

        try:
            actor = org.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied({'error': 'You are not allowed to do that'})

        if actor.role not in ["owner", "admin"]:
            raise PermissionDenied({'error': 'You are not allowed to do that'})

        member.delete()
        return Response({'message': 'Member was removed from the organization'})

# api/organizations/<int:org_pk>/projects
# api/organizations/<int:org_pk>/projects/<int:project_pk>
class OrganizationProjectManagementView(viewsets.ViewSet):
    def find(self, request: Request, org_pk, project_pk=None):
        authenticated = request.user.is_authenticated

        try:
            org = Organization.objects.get(id=org_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Organization not found"})

        if not authenticated:
            if org.private:
                raise NotAuthenticated({"error": "Authentication needed"})
            else:
                if not project_pk:
                    projects = org.projects.filter(
                        Q(secret=False) | Q(private=False)
                    ).distinct()
                    serializer = ProjectSerializer(projects, many=True)
                    return Response(serializer.data)
                else:
                    try:
                        project = org.projects.get(id=project_pk)

                        if project.secret or project.secret:
                            raise PermissionDenied({"error": "Not allowed"})

                        serializer = ProjectSerializer(project)
                        return Response(serializer.data)
                    except ObjectDoesNotExist:
                        raise NotFound({"error": "Project not found"})
        else:
            if not project_pk:
                projects = org.projects.filter(
                    Q(private=False) & Q(secret=False)
                ).distinct()
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data)
            else:
                try:
                    project = org.projects.get(id=project_pk)
                    if project.secret and not project.assignees.filter(member=request.user).exists():
                        raise PermissionDenied({"error": "Not allowed"})
                    serializer = ProjectSerializer(project)
                    return Response(serializer.data)
                except ObjectDoesNotExist:
                    raise NotFound({"error": "Project not found"})
