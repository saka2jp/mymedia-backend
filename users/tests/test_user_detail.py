import pytest
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

UserModel = get_user_model()
ApplicationModel = get_application_model()
AccessTokenModel = get_access_token_model()


@pytest.mark.django_db
class TestUserDetail:

    def setup_method(self, method):
        self.user = UserModel.objects.create_user('user', 'test@example.com', '123456')
        self.app = ApplicationModel.objects.create(
            name='app',
            client_type=ApplicationModel.CLIENT_CONFIDENTIAL,
            authorization_grant_type=ApplicationModel.GRANT_CLIENT_CREDENTIALS,
            user=self.user
        )
        self.token = AccessTokenModel.objects.create(
            user=self.user,
            token='lIN4xH5EU04HLM1NR1fFR9IHWTdWWM',
            application=self.app,
            expires=now()+timedelta(days=365)
        )
        self.client = APIClient()

    def test_get_ok_case(self):
        """ OK: GET /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        response = self.client.get(f'/users/{self.user.pk}/', **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == str(self.user)

    def test_put_ok_case(self):
        """ OK: PUT /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        body = {
            'username': 'test',
            'password': 'password'
        }
        response = self.client.put(f'/users/{self.user.pk}/', body, format='json', **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == 'test'

    def test_patch_ok_case(self):
        """ OK: PATCH /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        body = {
            'username': 'test'
        }
        response = self.client.patch(f'/users/{self.user.pk}/', body, format='json', **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == 'test'

    def test_delete_ok_case(self):
        """ OK: DELETE /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        response = self.client.delete(f'/users/{self.user.pk}/', **headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_bad_request_case(self):
        """ Bad Request: PUT /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        body = {
            'password': 'password'
        }
        response = self.client.put(f'/users/{self.user.pk}/', body, format='json', **headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthorized_case(self):
        """ Unauthorized: GET /users/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }
        response = self.client.get(f'/users/{self.user.pk}/', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
