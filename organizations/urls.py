from django.urls import path

from organizations.views import (
    OrganizationMemberManagementView,
    OrganizationManagementView,
    OrganizationProjectManagementView
)

addMember = OrganizationMemberManagementView.as_view({"post": "create"})
deleteMember = OrganizationMemberManagementView.as_view({"delete": "destroy"})

urlpatterns = [
    path("", OrganizationManagementView.as_view({"get": "get", "post": "post"}), name="organizationView"),
    path("<int:organization_pk>", OrganizationManagementView.as_view({"get": "get", "delete": "delete", "patch": "update"}), name="organizationViewId"),

    path("<int:organization_pk>/members", OrganizationMemberManagementView.as_view({"get": "get", "post": "post"}), name="memberManagement"),
    path("<int:organization_pk>/members/<int:member_pk>", OrganizationMemberManagementView.as_view({"delete": "delete"}), name="memberManagementId"),

    path("<int:organization_pk>/projects", OrganizationProjectManagementView.as_view({"get": "get"}), name="projectManagement"),
    path("<int:organization_pk>/projects/<int:project_pk>", OrganizationProjectManagementView.as_view({"get": "get"}), name="projectManagementId")
]
