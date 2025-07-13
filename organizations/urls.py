from django.urls import path

from organizations.views import (
    MemberManagementView,
    OrganizationView,
    get_organization_members,
)

addMember = MemberManagementView.as_view({"post": "create"})
deleteMember = MemberManagementView.as_view({"delete": "destroy"})

urlpatterns = [
    path("", OrganizationView.as_view(), name="get_organizations"),
    path(
        "<int:organization_id>", OrganizationView.as_view(), name="get_organization_id"
    ),
    path("", OrganizationView.as_view(), name="post_organization"),
    path("<int:pk>/members", get_organization_members, name="get_org_members"),
    path("<int:orgPk>/member", addMember, name="addMember"),
    path("<int:orgPk>/member/<int:memberPk>", deleteMember, name="memberManagement"),
]
