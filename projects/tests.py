from django.test import TestCase

from accounts.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project

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
