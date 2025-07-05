from django.urls import path
from .views import AccountManagement

urlpatterns = [
    path('', AccountManagement.as_view(), name='account_management'),
]