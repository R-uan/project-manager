from django.test import TestCase
from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project
from teams.models import Team, TeamMembership, TeamProject


class AccountsModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="User",
            password="Secr#t",
            first_name="Test",
            last_name="User",
        )

        self.user2 = User.objects.create_user(
            email="me2@gmail.com",
            username="User 2",
            password="Secr#t",
            first_name="User",
            last_name="Test",
        )

        self.organization = Organization.objects.create(
            name="Test Organization", owner=self.user, email="org@gmail.com"
        )

        self.organization2 = Organization.objects.create(
            name="Test Org", owner=self.user2, email="org2@gmail.com"
        )

        self.org_member = OrganizationMember.objects.create(
            organization=self.organization,
            member=self.user,
            role="owner",
        )

        self.org2_member = OrganizationMember.objects.create(
            organization=self.organization2, member=self.user2, role="owner"
        )

        self.org2_member2 = OrganizationMember.objects.create(
            organization=self.organization2, member=self.user, role="member"
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

    def test_get_user_owned_orgs(self):
        orgs = self.user.owned_organizations.all()
        self.assertEqual(len(orgs), 1)
        self.assertIsInstance(orgs[0], Organization)

    def test_get_user_my_memberships(self):
        orgs = self.user.memberships.all()
        self.assertEqual(len(orgs), 2)
        self.assertIsInstance(orgs[0], OrganizationMember)

    def test_get_user_organizations(self):
        orgs = self.user.organizations.all()
        self.assertEqual(len(orgs), 2)
        self.assertIsInstance(orgs[0], Organization)
