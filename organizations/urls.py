from django.urls import path

from organizations.views import OrganizationView, get_organization_members, post_organization_member


urlpatterns = [
    path("", OrganizationView.as_view(), name="get_organizations"),
    path("<int:organization_id>", OrganizationView.as_view(), name="get_organization_id"),
    path("", OrganizationView.as_view(), name="post_organization"),
    path("<int:pk>/members", get_organization_members, name="get_org_members"),
    path("<int:pk>/member", post_organization_member, name="post_member")
]
