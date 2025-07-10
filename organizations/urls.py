from django.urls import path

from organizations.views import OrganizationManagerView

urlpatterns = [
    path("", OrganizationManagerView.as_view(), name="get_organizations"),
    path(
        "<int:organization_id>",
        OrganizationManagerView.as_view(),
        name="get_organization_id",
    ),
    path("", OrganizationManagerView.as_view(), name="post_organization"),
]
