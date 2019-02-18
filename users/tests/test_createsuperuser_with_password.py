import pytest

from django.core.management import CommandError, call_command
from django.test.client import Client


@pytest.mark.django_db
class TestCreateSuperUserCommand:

    def setup_method(self, method):
        self.email = 'admin@example.com'
        self.password = 'admin'

    def test_success_case_createsuperuser_with_password(self):
        """Success"""
        call_command(
            'createsuperuser_with_password',
            '--email', self.email,
            '--password', self.password
        )
        client = Client()
        response = client.login(email=self.email, password=self.password)
        assert response is True

    def test_failure_case_createsuperuser_with_password(self):
        """Failure"""
        with pytest.raises(CommandError):
            call_command(
                'createsuperuser_with_password',
                '--email', self.email
            )
