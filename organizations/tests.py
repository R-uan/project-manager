from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project


# Create your tests here.


class OrganizationModelsTest(TestCase):
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


    def test_query_organization_projects(self):
        projects = self.organization.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertIsInstance(projects[0], Project)

    def test_query_organization_members(self):
        members = self.organization.members.all()
        self.assertEqual(len(members), 1)
        self.assertIsInstance(members[0], OrganizationMember)


class OrganizationViewsTest(APITestCase):
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
            member=self.userThree,
            role="member",
        )

        self.project = Project.objects.create(
            title="Silly Project", organization=self.organization
        )

        self.authenticatedClient = APIClient()
        self.authenticatedClientTwo = APIClient()
        self.authenticatedClientTwo.force_authenticate(user=self.userTwo)
        self.authenticatedClient.force_authenticate(user=self.user)
        self.unauthenticatedClient = APIClient()

    def test_post_organization(self):
        payload = {"name": "Testing Org", "private": False, "email": "capybara@org.com"}
        response = self.authenticatedClient.post(reverse("organizationView"), payload)
        self.assertEqual(response.status_code, 200)

    def test_get_organizations(self):
        response = self.authenticatedClient.get(reverse("organizationView"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_get_organizations_members(self):
        response = self.authenticatedClient.get(reverse("memberManagement", kwargs={"org_pk": self.organization.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_get_private_organization_members(self):
        response = self.authenticatedClientTwo.get(reverse("memberManagement", kwargs={"org_pk": self.organization.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_unauthorized_organization_members(self):
        response = self.unauthenticatedClient.get(reverse("memberManagement", kwargs={"org_pk": self.organization.id}))
        self.assertEqual(response.status_code, 401)

    def test_post_member(self):
        payload = {"member_pk": self.userTwo.id, "role": "member"}
        response = self.authenticatedClient.post(reverse("memberManagement", kwargs={"org_pk": self.organization.id}), payload)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_delete_member(self):
        response = self.unauthenticatedClient.delete(reverse("memberManagementId", kwargs={'org_pk': self.organization.id, 'member_pk': self.userTwo.id}))
        self.assertEqual(response.status_code, 401)

    def test_delete_member(self):
        response = self.authenticatedClient.delete(reverse("memberManagementId", kwargs={'org_pk': self.organization.id, 'member_pk': self.userThree.id}))
        self.assertEqual(response.status_code, 200)

    def test_member_delete_member(self):
        response = self.authenticatedClientTwo.delete(reverse("memberManagementId", kwargs={'org_pk': self.organization.id, 'member_pk': self.user.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_projects(self):
        response = self.authenticatedClient.get(reverse("projectManagement", kwargs={"org_pk": self.organization.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_project_by_id(self):
        response = self.authenticatedClient.get(reverse("projectManagementId", kwargs={"org_pk": self.organization.id, "project_pk": self.project.id}))
        self.assertEqual(response.status_code, 200)
