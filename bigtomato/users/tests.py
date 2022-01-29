from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class TestUserEndpoints(TestCase):
    @property
    def default_user_params(self):
        return {
            "username": "test_username",
            "password": "test_password",
            "name": "test_myname",
            "email": "test@test.com",
        }

    def test_create_user_endpoint_success(self):
        params = self.default_user_params
        client = Client()

        response = client.post("/users/", params)

        assert response.status_code == 201
        assert User.objects.count() > 0, "Create user endpoint should create a user"

    def test_create_user_endpoint_with_invalid_params(self):
        params = self.default_user_params
        params.update({"email": "whohoho"})
        client = Client()

        response = client.post("/users/", params)

        assert response.status_code == 400, "should not be able to create user with bad email"

        params.update({"email": "test@test.com", "password": "a"})
        response = client.post("/users/", params)

        assert response.status_code == 400, "should not be able to create user with short password"

        params.update({"password": "test_password", "username": ""})
        response = client.post("/users/", params)

        assert response.status_code == 400, "should not be able to create user with empty username"

    def test_get_user_endpoint_success(self):
        params = self.default_user_params
        params.pop("name")
        user = User.objects.create_user(**params)
        self.client.force_login(user)
        url = reverse("user-list")

        response = self.client.get(url)

        assert response.status_code == 200

    def test_get_user_endpoint_without_authorization(self):
        url = reverse("user-list")

        response = self.client.get(url)

        assert response.status_code == 401, "Get user should return 401 when no authorization is supplied"
