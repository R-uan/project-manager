from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from organizations.models import Organization
from projects.models import Project, ProjectAssignment
from projects.serializers import NewProjectSerializer, ProjectSerializer, UpdateProjectSerializer, AssignProjectMember


class ProjectManagerView(viewsets.ViewSet):
    def new_project(self, request: Request):
        if not request.user.is_authenticated:
            raise NotAuthenticated({"error": "Authentication needed"})
        data = NewProjectSerializer(data=request.data)
        if not data.is_valid():
            raise BadRequest(data.errors)

        try:
            org_pk = data.validated_data["organization"]
            organization = Organization.objects.get(id=org_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Organization was not found"})
        except IntegrityError:
            raise BadRequest({"error": "Organization Id invalid"})

        try:
            member = organization.members.get(member=request.user)
            if member.role not in ["admin", "owner"]:
                raise PermissionDenied({"error": "You're not allowed to do that"})
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You're not allowed to do that"})

        project = Project.objects.create(
            organization=organization,
            title=data.validated_data["title"],
            secret=data.validated_data["secret"],
            private=data.validated_data["private"],
            status=data.validated_data["status"],
        )

        return Response({"message": f"{project.id} created"})

    def get_project(self, request: Request, project_pk):
        try:
            project = Project.objects.get(id=project_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Project was not found"})

        if project.private:
            if not request.user.is_authenticated:
                raise NotAuthenticated({"error": "Authentication needed"})
            try:
                org_member = project.organization.members.get(member=request.user)
            except ObjectDoesNotExist:
                raise PermissionDenied({"error": "You can't see this"})
            if project.secret and not project.assignees.filter(member=request.user).exists():
                raise PermissionDenied({"error": "You can't see this"})

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def delete_project(self, request: Request, project_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated({"error": "Authentication needed"})

        try:
            project = Project.objects.get(id=project_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Project was not found"})

        try:
            member = project.organization.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        if member.role not in ["owner", "admin"]:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        project.delete()
        return Response({"message": f"Project {project.id} was deleted"})

    def update_project(self, request: Request, project_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated({"error": "Authentication needed"})

        serialize = UpdateProjectSerializer(data=request.data)
        if not serialize.is_valid(): raise BadRequest(serialize.errors)
        data = serialize.validated_data

        try:
            project = Project.objects.get(id=project_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Project was not found"})

        try:
            member = project.organization.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        if member.role not in ["owner", "admin"]:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        if data["title"]:
            project.title = data["title"]
        if data["secret"]:
            project.secret = data["secret"]
        if data["private"]:
            project.private = data["private"]
        if project["status"]:
            project.status = data["status"]

        project.save()
        return Response({"message": f"Project {project.id} updated"})

class ProjectAssigneesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def assign_member(self, request: Request, project_pk):
        serialize = AssignProjectMember(data=request.data)
        if not serialize.is_valid(): raise BadRequest(serialize.errors)
        body = serialize.validated_data

        try:
            project = Project.objects.get(id=project_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Project was not found"})

        try:
            user = project.organization.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        if user.role not in ["owner", "admin"]:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        try:
            member = project.organization.members.get(id=body["member_pk"])
        except ObjectDoesNotExist:
            raise NotFound({"error": "Member was not found"})

        ProjectAssignment.objects.create(
            member=member,
            project=project
        )

        return Response({"message": "Member assigned to project"})


    def unassign_member(self, request: Request, project_pk):
        serialize = AssignProjectMember(data=request.data)
        if not serialize.is_valid(): raise BadRequest(serialize.errors)
        body = serialize.validated_data

        try:
            project = Project.objects.get(id=project_pk)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Project was not found"})

        try:
            user = project.organization.members.get(member=request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        if user.role not in ["owner", "admin"]:
            raise PermissionDenied({"error": "You are not allowed to do that"})

        try:
            member = project.organization.members.get(id=body["member_pk"])
        except ObjectDoesNotExist:
            raise NotFound({"error": "Member was not found"})

        try:
            assignment = project.assignees.get(member=member)
        except ObjectDoesNotExist:
            raise NotFound({"error": "Member is not assigned to project"})

        assignment.delete()

        return Response({"message": "Member unassigned from project"})