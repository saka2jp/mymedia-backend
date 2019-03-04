import pytest
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

from ..factories import BlogFactory

UserModel = get_user_model()
ApplicationModel = get_application_model()
AccessTokenModel = get_access_token_model()


@pytest.mark.django_db
class TestBlogDetail:

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
        self.data = {
            'title': 'Test',
            'url': 'https://example.com/test/',
            'thumbnail': 'https://example.com/thumbnail.jpg',
            'start_dt': '2019-03-01T00:00:00+09:00',
            'end_dt': '2019-03-31T00:00:00+09:00',
            'is_public': True
        }

    def test_get_ok_case(self):
        """ OK: GET /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        response = self.client.get(f'/blogs/{blog.pk}/', **headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get_unauthorized_case(self):
        """ Unauthorized: GET /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }

        response = self.client.get(f'/blogs/{blog.pk}/', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_not_found_case(self):
        """ Not Found: GET /blogs/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        response = self.client.get('/blogs/1/', **headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_ok_case(self):
        """ OK: PUT /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        self.data['title'] = 'Updated'
        response = self.client.put(f'/blogs/{blog.pk}/', self.data, **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'Updated'

    def test_put_unauthorized_case(self):
        """ Unauthorized: PUT /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }

        self.data['title'] = 'Updated'
        response = self.client.put(f'/blogs/{blog.pk}/', self.data, **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_not_found_case(self):
        """ Not Found: PUT /blogs/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        self.data['title'] = 'Updated'
        response = self.client.put('/blogs/1/', self.data, **headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_ok_case(self):
        """ OK: PATCH /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        data = dict(title='Updated')
        response = self.client.patch(f'/blogs/{blog.pk}/', data, **headers)
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'Updated'

    def test_patch_unauthorized_case(self):
        """ Unauthorized: PATCH /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }

        data = dict(title='Updated')
        response = self.client.patch(f'/blogs/{blog.pk}/', data, **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_not_found_case(self):
        """ Not Found: PATCH /blogs/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        data = dict(title='Updated')
        response = self.client.patch('/blogs/1/', data, **headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_ok_case(self):
        """ OK: DELETE /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        response = self.client.delete(f'/blogs/{blog.pk}/', **headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_unauthorized_case(self):
        """ Unauthorized: DELETE /blogs/<int:pk>/ """
        blog = BlogFactory(**self.data)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'badtoken',
        }

        response = self.client.delete(f'/blogs/{blog.pk}/', **headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_not_found_case(self):
        """ Not Found: DELETE /blogs/<int:pk>/ """
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(self.token),
        }

        response = self.client.get('/blogs/1/', **headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
