from django.test import TestCase
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

    def test_query_team_projects(self):
        projects = self.team.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertIsInstance(projects[0], Project)

    def test_query_team_members(self):
        members = self.team.members.all()
        self.assertEqual(len(members), 1)
        self.assertIsInstance(members[0], OrganizationMember)
