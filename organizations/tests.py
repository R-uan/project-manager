from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project
from teams.models import Team, TeamMembership, TeamProject

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

        self.team = Team.objects.create(
            organization=self.organization,
            name="Silly Team",
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.org_member,
        )

        self.project = Project.objects.create(
            title="Silly Project", organization=self.organization
        )

        TeamProject.objects.create(team=self.team, project=self.project)

    def test_query_organization_teams(self):
        teams = self.organization.teams.all()
        self.assertEqual(len(teams), 1)
        self.assertIsInstance(teams[0], Team)

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

        self.organization = Organization.objects.create(
            name="Test Organization", owner=self.user, email="org@gmail.com"
        )

        self.org_member = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.user,
            role="owner",
        )

        self.team = Team.objects.create(
            organization=self.organization,
            name="Silly Team",
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.org_member,
        )

        self.project = Project.objects.create(
            title="Silly Project", organization=self.organization
        )

        TeamProject.objects.create(team=self.team, project=self.project)

        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)
        self.unauthenticated_client = APIClient()

    def test_post_organization(self):
        payload = {"name": "Testing Org", "private": False, "email": "capybara@org.com"}
        response = self.authenticated_client.post(reverse("post_organization"), payload)
        self.assertEqual(response.status_code, 200)

    def test_get_organizations(self):
        response = self.authenticated_client.get(reverse('get_organizations'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
