from django.test import TestCase

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
            last_name="User"
        )
        
        self.organization = Organization.objects.create(
            name="Test Organization",
            owner=self.user,
            email="org@gmail.com"    
        )

        self.org_member = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.user,
            role='owner',
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
            title="Silly Project",
            organization=self.organization
        )

        TeamProject.objects.create(
            team=self.team,
            project=self.project
        )

    def test_query_organization_teams(self):
        teams = self.organization.teams.all()
        self.assertEqual(len(teams), 1)
        self.assertIsInstance(teams[0], Team)

    def test_query_organization_projects(self):
        projects = self.organization.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertIsInstance(projects[0], Project)
