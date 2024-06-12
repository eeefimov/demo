"""
This module contains tests for PATCH /auth/register endpoint.

[tests DEFINITIONS]:
    Post request for /auth/register endpoint.
    Patch request for /auth/user endpoint.
    Get request for /auth/user endpoint.
[tests FEATURES]:
    Verify response status code ('email': 200).
    Verify response status code ('name': 200).
    Verify response status code ('password': 200).
    Verify exist of payload in response ('email': 200).
    Verify exist of payload in response ('name': 200).
    Verify exist of payload in response ('password': 200).
    Verify types values in response ('email': 200).
    Verify types values in response ('name': 200).
    Verify types values in response ('password': 200).
    Verify updates of user credentials ('email': 200).
    Verify updates of user credentials ('name': 200).
    Verify updates of user credentials ('password': 200).
    Verify response with invalid token ('email', Empty token: 401).
    Verify response with invalid token ('email', Invalid token: 401).
    Verify response with invalid token ('name', Empty token: 401).
    Verify response with invalid token ('name', Invalid token: 401).
    Verify response with invalid token ('password', Empty token: 401).
    Verify response with invalid token ('password',Invalid token: 401).
    Verify response code with exist email patch.
"""
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
import pytest
from data_models.user_model import UserModel, MsgModel
from params_api.api_user_params import invalid_token, \
    patch_valid


class TestPatchUser:
    """Class for testing Patch /auth/user endpoint."""
    @pytest.mark.parametrize('value, exp', patch_valid)
    def test_status_code(self, usr, value, exp):
        """Verify response status code."""
        response = usr.patch_user(usr.new_user_data(value))
        assert response.status_code == exp

    @pytest.mark.parametrize('value, exp', patch_valid)
    def test_response_payload(self, usr, value, exp):
        """Verify exist of payload in response."""
        response = usr.patch_user(usr.new_user_data(value))
        assert response.json()

    @pytest.mark.parametrize('value, exp', patch_valid)
    def test_payload_type_validation(self, usr, value, exp):
        """Verify types values in response."""
        response = usr.patch_user(usr.new_user_data(value))
        model = usr.get_model(UserModel, response.json())
        assert isinstance(model, UserModel)

    @pytest.mark.parametrize('value, exp', patch_valid)
    def test_update_credentials_validation(self, usr, value, exp):
        """Verify updates of user credentials."""
        old_data = usr.data
        response = usr.patch_user(usr.new_user_data(value))
        assert response.status_code == exp
        assert old_data != usr.data

    @pytest.mark.parametrize('value, exp_v', patch_valid)
    @pytest.mark.parametrize("token, exp", invalid_token)
    def test_invalid_token(self, usr, token, exp, value, exp_v):
        """Verify response with invalid token."""
        usr.header = usr.header_auth(token)
        response = usr.patch_user(usr.new_user_data(value))
        assert response.status_code == exp
        model = usr.get_model(MsgModel, response.json())
        expected_model = usr.get_model(MsgModel, usr.authorisation)
        assert model == expected_model

    def test_exist_email_validation(self, usr):
        """Verify response code with exist email patch."""
        mail = {'email': usr.data['email']}
        response = usr.patch_user(mail)
        assert response.status_code == 403
