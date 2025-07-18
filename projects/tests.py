from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project
from rest_framework.test import APITestCase, APIClient


# Create your tests here.


class ProjectsModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="User",
            password="Secr#t",
            first_name="Test",
            last_name="User",
        )

        self.organization = Organization.objects.create(
            name="Test Organization", owner=self.user, email="org@gmail.com"
        )

        self.org_member = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.user,
            role="owner",
        )

        self.project = Project.objects.create(
            title="Silly Project", organization=self.organization
        )

    def test_query_project_tasks(self):
        tasks = self.project.tasks.all()
        self.assertEqual(len(tasks), 0)

class ProjectManageViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="User",
            password="Secr#t",
            first_name="Test",
            last_name="User",
        )

        self.userTwo = User.objects.create(
            email="me2@gmail.com",
            username="User2",
            password="Secr#t",
            first_name="Test2",
            last_name="User2",
        )

        self.userThree = User.objects.create(
            email="me3@gmail.com",
            username="User3",
            password="Secr#t",
            first_name="Test2",
            last_name="User2",
        )

        self.organization = Organization.objects.create(
            name="Test Organization",
            owner=self.user,
            email="org@gmail.com",
            private=True,
        )

        self.orgMember = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.user,
            role="owner",
        )

        self.orgMemberTwo = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.userTwo,
            role="member",
        )

        self.project = Project.objects.create(
            title="Silly Project", organization=self.organization
        )

        self.projectTwo = Project.objects.create(
            title="Silly Project 2", organization=self.organization, private=True, secret=True
        )

        self.authenticatedClient = APIClient()
        self.authenticatedClientTwo = APIClient()
        self.authenticatedClientTwo.force_authenticate(user=self.userTwo)
        self.authenticatedClient.force_authenticate(user=self.user)
        self.unauthenticatedClient = APIClient()

    def test_get_project(self):
        response = self.authenticatedClient.get(reverse("projects_id", kwargs={"project_pk": self.project.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.project.title)

    def test_get_private_project(self):
        response = self.unauthenticatedClient.get(reverse("projects_id", kwargs={"project_pk": self.projectTwo.id}))
        self.assertEqual(response.status_code, 401)

    def test_get_secret_project(self):
        response = self.authenticatedClientTwo.get(reverse("projects_id", kwargs={"project_pk": self.projectTwo.id}))
        self.assertEqual(response.status_code, 403)

    def test_create_project(self):
        payload = {
            "organization": self.organization.id,
            "title": "Project Test",
        }

        response = self.authenticatedClient.post(reverse("projects"), payload)
        self.assertEqual(response.status_code, 200)

    def test_create_project_unauthorized(self):
        payload = {
            "organization": self.organization.id,
            "title": "Project Test",
        }

        response = self.unauthenticatedClient.post(reverse("projects"), payload)
        self.assertEqual(response.status_code, 401)

    def test_create_project_not_admin(self):
        payload = {
            "organization": self.organization.id,
            "title": "Project Test",
        }

        response = self.authenticatedClientTwo.post(reverse("projects"), payload)
        self.assertEqual(response.status_code, 403)

    def test_delete_project_not_admin(self):
        response = self.authenticatedClientTwo.delete(reverse("projects_id", kwargs={"project_pk": self.project.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_project_owner(self):
        response = self.authenticatedClient.delete(reverse("projects_id", kwargs={"project_pk": self.project.id}))
        self.assertEqual(response.status_code, 200)
