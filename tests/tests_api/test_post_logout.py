"""
This module contains tests for POST /auth/logout endpoint.

[tests DEFINITIONS]:
    Post request for /auth/logout endpoint.
    Post request for /auth/register endpoint.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify payload values in response.
    Verify response code with invalid token (Empty token: 401).
    Verify response code with invalid token (Invalid token: 401).
    Verify response with invalid token (Empty token: 401).
    Verify response with invalid token (Empty token: 401).
    Verify response code with invalid methods (GET: 404).
    Verify response code with invalid methods (PUT: 404).
    Verify response code with invalid methods (PATCH: 404).
"""
import pytest
from data_models.user_model import MsgModel
from params_api.api_user_params import invalid_token
from params_api.api_register_params import invalid_methods


class TestPostLogout:
    """Class for testing Post /auth/logout endpoint."""
    def test_status_code(self, logout):
        """Verify response status code."""
        response = logout.post_logout(logout.access_token)
        assert response.status_code == 200

    def test_response_payload(self, logout):
        """Verify exist of payload in response."""
        response = logout.post_logout(logout.access_token)
        assert response.json()

    def test_payload_type_validation(self, logout):
        """Verify payload values in response."""
        response = logout.post_logout(logout.access_token)
        model_response = logout.get_model(MsgModel, response.json())
        expected_model = logout.get_model(MsgModel, logout.successful_logout)
        assert model_response == expected_model

    @pytest.mark.parametrize("token, exp", invalid_token)
    def test_invalid_token(self, logout, token, exp):
        """Verify response code with invalid token."""
        response = logout.post_logout(token)
        assert response.status_code in (exp, 404)

    @pytest.mark.parametrize("token, exp", invalid_token)
    def test_invalid_token_payload_validation(self, logout, token, exp):
        """Verify response with invalid token."""
        response = logout.post_logout(token)
        model_response = logout.get_model(MsgModel, response.json())
        expected_model = logout.get_model(MsgModel, logout.toke_required)
        assert response.status_code in (exp, 404)
        assert model_response == expected_model

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, logout, method, exp):
        """Verify response code with invalid methods."""
        logout.setup_logout(logout.access_token)
        response = logout.send_requests(method, logout.endpoints.logout,
                                        None, logout.data)
        assert response.status_code == exp
        logout.attach_response(response.text)
