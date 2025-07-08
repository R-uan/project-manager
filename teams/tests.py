from projects.models import Project, ProjectTeam
from projects.serializers import ProjectSerializer
from .models import Team, TeamMembership
from django.urls import reverse
from accounts.models import User
from rest_framework.test import APITestCase, APIClient


# Create your tests here.

class TeamOwnershipManagementViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="test_user",
            password="secret",
            first_name="Me",
            last_name="Moi"
        )

        self.user2 = User.objects.create_user(
            email="me2@gmail.com",
            username="test_user2",
            password="secret",
            first_name="Me2",
            last_name="Moi2"
        )

        self.unauthorized_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)

        self.authorized_client_2 = APIClient()
        self.authorized_client_2.force_authenticate(user=self.user2)

    # post
    def test_post_team(self):
        payload = {'name': 'test_team', 'private': False}
        response = self.authorized_client.post(reverse('owned_team_management'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Team created')

    # get
    def test_get_owned_teams(self):
        Team.objects.create(
            name="Test Get Team",
            private=False,
            owner=self.user2
        )

        Team.objects.create(
            name="Test Get Team 2",
            private=False,
            owner=self.user2
        )

        response = self.authorized_client_2.get(reverse('owned_team_management'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(2, len(response.data))

    def test_get_owned_teams_not_authorized(self):
        response = self.unauthorized_client.get(reverse('owned_team_management'))
        self.assertEqual(response.status_code, 401)

    # get/id
    def test_get_owned_team_by_id(self):
        team = Team.objects.create(
            name="TestingIDGet",
            private=False,
            owner=self.user2
        )

        response = self.authorized_client_2.get(reverse('owned_team_management_id', kwargs={'team_id': team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'TestingIDGet')

    def test_get_owned_team_by_id_not_found(self):
        response = self.authorized_client_2.get(reverse('owned_team_management_id', kwargs={'team_id': 6}))
        self.assertEqual(response.status_code, 404)

    def test_get_owned_team_by_id_forbidden(self):
        team = Team.objects.create(
            name="Test Delete",
            private=True,
            owner=self.user
        )

        response = self.authorized_client_2.get(reverse('owned_team_management_id', kwargs={'team_id': team.id}))
        self.assertEqual(response.status_code, 403)

    # delete
    def test_delete_owned_team_with_id(self):
        team = Team.objects.create(
            name="Test Delete",
            private=False,
            owner=self.user
        )

        response = self.authorized_client.delete(reverse('owned_team_management_id', kwargs={'team_id': team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Team successfully deleted')

    def test_delete_owned_team_with_id_forbidden(self):
        team = Team.objects.create(
            name="Test Delete",
            private=False,
            owner=self.user2
        )

        response = self.authorized_client.delete(reverse('owned_team_management_id', kwargs={'team_id': team.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_owned_team_with_id_not_found(self):
        response = self.authorized_client.delete(reverse('owned_team_management_id', kwargs={'team_id': 69}))
        self.assertEqual(response.status_code, 404)

class TeamProjectsManagerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="me@gmail.com",
            username="test_user",
            password="secret",
            first_name="Me",
            last_name="Moi"
        )

        self.team = Team.objects.create(
          name="Team Test",
          private=False,
          owner=self.user  
        )

        TeamMembership.objects.create(
            team = self.team,
            user = self.user,
            role = 'owner'
        )

        self.project = Project.objects.create(
            title="Project Test",
            private=True,
        )

        self.project2 = Project.objects.create(
            title="Project Test 2",
            private=False
        )

        ProjectTeam.objects.create(
            team=self.team,
            project=self.project
        )

        ProjectTeam.objects.create(
            team=self.team,
            project=self.project2
        )
        
        self.user2 = User.objects.create_user(
            email="me2@gmail.com",
            username="test_user2",
            password="secret",
            first_name="Me2",
            last_name="Moi2"
        )

        self.unauthorized_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)

        self.authorized_client_2 = APIClient()
        self.authorized_client_2.force_authenticate(user=self.user2)


    def test_get_team_projects_from_orm(self):
        projects = self.team.projects.all()
        self.assertEqual(len(projects), 2)

    def test_get_project_instance_from_orm(self):
        project = self.team.projects.get(id=self.project.id)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.title, 'Project Test')

    def test_get_team_projects(self):
        response = self.authorized_client.get(reverse('team_projects', kwargs={'team_id': self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_get_team_projects_while_unauthorized(self):
        response = self.unauthorized_client.get(reverse('team_projects', kwargs={'team_id': self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_get_team_projects_by_id_while_unauthorized(self):
        response = self.unauthorized_client.get(reverse('team_projects_id', kwargs={'team_id': self.team.id, 'project_id': self.project.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_team_project_by_id_while_not_member_authenticated(self):
        response = self.authorized_client_2.get(reverse('team_projects_id', kwargs={'team_id': self.team.id, 'project_id': self.project.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_team_project_by_id_while_authenticated(self):
        response = self.authorized_client.get(reverse('team_projects_id', kwargs={'team_id': self.team.id, 'project_id': self.project.id}))
        self.assertEqual(response.status_code, 200)
        expected = ProjectSerializer(self.project)
        self.assertEqual(response.data, expected.data)
