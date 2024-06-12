"""
This module contains tests for POST /password-reset endpoint.

[tests DEFINITIONS]:
    Post request for /password-reset endpoint.
    Post request for /auth/register endpoint.
    User access_token.
    access to user gmail box.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify values in response.
    Verify reset code in email box (Not registered email).
    Verify reset code in email box (Registered email).
    Verify response code with invalid type of method (GET: 404).
    Verify response code with invalid type of method (PUT: 404).
    Verify response code with invalid type of method (PATCH: 404).
"""
import pytest
from data_models.user_model import MsgModel
from tests.utils import UTILS
from pages.reset_page_class import RESET
from params_api.api_reset_params import email_send_code
from params_api.api_register_params import invalid_methods


class TestReset:
    """Class for testing Post /password-reset endpoint."""
    def test_status_code(self, reset):
        """Verify response status code."""
        response = reset.send_requests('post', reset.endpoint,
                                       None, reset.data)
        assert response.status_code
        reset.attach_response(response)

    def test_response_payload(self, reset):
        """Verify exist of payload in response."""
        response = reset.send_requests('post', reset.endpoint,
                                       None, reset.data)
        assert response.json()
        reset.attach_response(response)

    def test_payload_validation(self, reset):
        """Verify values in response."""
        response = reset.send_requests('post', reset.endpoint,
                                       None, reset.data)
        model = reset.get_model(MsgModel, response.json())
        model_expected = reset.get_model(MsgModel,
                                         reset.reset_sent)
        assert model == model_expected

    @pytest.mark.parametrize('mail, pwd', email_send_code)
    def test_reset_code(self, reset, mail, pwd):
        """Verify reset code in email box."""
        reset.data = {"email": f"{mail}"}
        response = reset.send_requests('post', reset.endpoint,
                                       None, reset.data)
        _, code = UTILS.mail_check(mail, pwd)
        assert code
        assert RESET.verify_confirmation_code(code)
        reset.attach_response(response)

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, reset, method, exp):
        """Verify response code with invalid type of method."""
        response = reset.send_requests(method, reset.endpoint,
                                       None, reset.data)
        assert response.status_code == exp
        reset.attach_response(response.text)
