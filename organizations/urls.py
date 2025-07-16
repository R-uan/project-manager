from django.urls import path

from organizations.views import (
    OrganizationMemberManagementView,
    OrganizationView,
    OrganizationProjectManagementView
)

addMember = OrganizationMemberManagementView.as_view({"post": "create"})
deleteMember = OrganizationMemberManagementView.as_view({"delete": "destroy"})

urlpatterns = [
    path("", OrganizationView.as_view({"get": "get", "post": "post"}), name="organizationView"),
    path("<int:organization_id>", OrganizationView.as_view({"get": "get", "delete": "delete"}), name="organizationViewId"),

    path("<int:org_pk>/members", OrganizationMemberManagementView.as_view({"get": "members", "post": "create"}), name="memberManagement"),
    path("<int:org_pk>/members/<int:member_pk>", OrganizationMemberManagementView.as_view({"delete": "destroy"}), name="memberManagementId"),

    path("<int:org_pk>/projects", OrganizationProjectManagementView.as_view({"get": "retrieval"}), name="projectManagement"),
    path("<int:org_pk>/projects/<int:project_pk>", OrganizationProjectManagementView.as_view({"get": "retrieval"}), name="projectManagementId")
]
