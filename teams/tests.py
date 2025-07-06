from django.test import TestCase
from .models import Team
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
            name="TestGET",
            private=False,
            owner=self.user2
        )

        Team.objects.create(
            name="TestGET2",
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
