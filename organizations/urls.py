from django.urls import path

from organizations.views import OrganizationView, get_organization_members


urlpatterns = [
    path("", OrganizationView.as_view(), name="get_organizations"),
    path("<int:organization_id>", OrganizationView.as_view(), name="get_organization_id"),
    path("", OrganizationView.as_view(), name="post_organization"),
    path("/members/<int:pk>", get_organization_members, name="get_org_members")
]
