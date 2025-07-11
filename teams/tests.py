from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from organizations.models import Organization, OrganizationMember
from projects.models import Project
from .models import Team, TeamMembership, TeamProject
from accounts.models import User

# Create your tests here.

class TeamModelsTest(TestCase):
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

    def test_query_team_projects(self):
        projects = self.team.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertIsInstance(projects[0], Project)

    def test_query_team_members(self):
        members = self.team.members.all()
        self.assertEqual(len(members), 1)
        self.assertIsInstance(members[0], OrganizationMember)



class TeamManagementView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="User",
            password="Secr#t",
            first_name="Test",
            last_name="User",
        )

        self.organization = Organization.objects.create(
            name="Test Organization", owner=self.user, email="org@gmail.com", private=True
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
        self.authenticated_client2 = APIClient()
        self.authenticated_client2.force_authenticate(user=User.objects.create(
            email="me2@gmail.com",
            username="User2",
            password="Secr#t",
            first_name="Test2",
            last_name="User2",
                                                        
        ))
        self.unauthenticated_client = APIClient()

    def test_get_team(self):
        response = self.authenticated_client.get(reverse('team_management', kwargs={'pk': self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.team.name)

    def test_get_private_team(self):
        response = self.unauthenticated_client.get(reverse('team_management', kwargs={'pk':self.team.id}))
        self.assertEqual(response.status_code, 401)

    def test_get_private_team_2(self):
        response = self.authenticated_client2.get(reverse('team_management', kwargs={'pk':self.team.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_private_team(self):
        response = self.unauthenticated_client.delete(reverse('team_management', kwargs={'pk':self.team.id}))
        self.assertEqual(response.status_code, 401)

    def test_delete_team(self):
        response = self.authenticated_client.delete(reverse('team_management', kwargs={'pk': self.team.id}))
        self.assertEqual(response.status_code, 204)
