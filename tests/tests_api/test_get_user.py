"""
This module contains tests for GET /auth/user endpoint.

[tests DEFINITIONS]:
    Get request for /auth/user endpoint.
    Post request for /auth/register endpoint.
    User access_token.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify types values in response.
    Verify user credentials in response.
    Verify response with invalid token (Empty token: 401).
    Verify response with invalid token (Invalid token: 401).
    Verify response code with invalid methods (POST: 403).
    Verify response code with invalid methods (PUT: 404).
"""
import allure
import pytest
from data_models.user_model import UserModel, MsgModel
from params_api.api_user_params import invalid_token, invalid_methods


class TestGetUser:
    """Class for testing Get /auth/user endpoint."""
    def test_status_code(self, usr):
        """Verify response status code."""
        response = usr.get_user()
        assert response.status_code == 200

    def test_response_payload(self, usr):
        """Verify exist of payload in response."""
        response = usr.get_user()
        assert response.json()

    def test_payload_type_validation(self, usr):
        """Verify types values in response."""
        response = usr.get_user()
        model = usr.get_model(UserModel, response.json())
        assert isinstance(model, UserModel)

    def test_payload_credentials_validation(self, usr):
        """Verify user credentials in response."""
        response = usr.get_user()
        assert usr.data['email'].lower() in response.json()['user']['email']
        assert usr.data['name'] in response.json()['user']['name']

    @pytest.mark.parametrize("token, exp", invalid_token)
    def test_invalid_token(self, usr, token, exp):
        """Verify response with invalid token."""
        with allure.step('Setup header with token'):
            usr.header = usr.header_auth(token)
        response = usr.get_user()
        assert response.status_code == exp
        model_response = usr.get_model(MsgModel, response.json())
        model_expected = usr.get_model(MsgModel, usr.authorisation)
        assert model_response == model_expected

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, usr, method, exp):
        """Verify response code with invalid methods."""
        response = usr.send_requests(method, usr.endpoint,
                                     usr.header, None)
        assert response.status_code == exp
        usr.attach_response(response.text)
