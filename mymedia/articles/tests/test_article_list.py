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
class TestArticleList:

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
        """ OK: GET /articles/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        response = self.client.get('/articles/', **headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get_ok_case_filtering(self):
        """ OK: GET /blogs/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        response = self.client.get('/articles/?is_public=true', **headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get_unauthorized_case(self):
        """ Unauthorized: GET /articles/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }
        response = self.client.get('/articles/', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_ok_case(self):
        """ OK: POST /articles/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        body = {
            'title': 'Test',
            'url': 'https://example.com/article_page',
            'thumbnail': 'https://example.com/thumbnail',
            'start_dt': '2019-03-01T00:00',
            'end_dt': '2019-03-01T00:00',
            'is_public': True,
        }
        response = self.client.post('/articles/', body, format='json', **headers)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == 'Test'

    def test_post_bad_request_case(self):
        """ Bad Request: POST /articles/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }
        body = {
            'url': 'https://example.com/article_page',
            'thumbnail': 'https://example.com/thumbnail',
            'start_dt': '2019-03-01T00:00',
            'end_dt': '2019-03-01T00:00',
            'is_public': True,
        }
        response = self.client.post('/articles/', body, format='json', **headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_unauthorized_case(self):
        """ Unauthorized: POST /articles/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }
        body = {
            'title': 'Test',
            'url': 'https://example.com/article_page',
            'thumbnail': 'https://example.com/thumbnail',
            'start_dt': '2019-03-01T00:00',
            'end_dt': '2019-03-01T00:00',
            'is_public': True,
        }
        response = self.client.post('/articles/', body, format='json', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
