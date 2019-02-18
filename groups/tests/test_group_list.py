import pytest
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.timezone import now, timedelta

UserModel = get_user_model()
ApplicationModel = get_application_model()
AccessTokenModel = get_access_token_model()


@pytest.mark.django_db
class TestGroupList:

    def setup_method(self, method):
        self.user = UserModel.objects.create_user('test@example.com', '123456')
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
        """ OK: GET /groups/ """
        Group.objects.create(name='test')
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        response = self.client.get('/groups/', **headers)
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{'name': 'test'}]

    def test_unauthorized_case(self):
        """ Unauthorized: GET /groups/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }
        response = self.client.get('/groups/', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
