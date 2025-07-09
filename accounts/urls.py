from django.urls import path
from .views import AccountManagement, get_organizations, get_owned_organizations

urlpatterns = [
    path("", AccountManagement.as_view(), name="account_management"),
    path("organizations", get_organizations, name="get_all_organizations"),
    path(
        "organizations/owned", get_owned_organizations, name="get_owned_organizations"
    ),
]
