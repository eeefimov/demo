"""
[tests AMOUNT]: 34
[tests DEFINITIONS]:
    Get request for /auth/user endpoint.
    Post request for /auth/register endpoint.
    User access_token.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify values type in response.
    Verify response code with empty credentials.
    Verify response code with invalid types of method.
    Verify response code with invalid type of body.
    Verify response code with different email.
    Verify response code with different password length.
    Verify response code with different name.
    Verify response with exist user registration.
"""
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
import allure
import pytest
from data_models.user_model import RegisterModel, MsgModel
from params_api.api_register_params import empty_register_credentials, \
    invalid_methods, invalid_data, invalid_email_format, \
    valid_email_formats, password_validation, name_validation


class TestRegister:
    """Class for testing Post /auth/register endpoint."""
    def test_status_code(self, register):
        """Verify response status code."""
        response = register.post_register()
        assert response.status_code == 200

    def test_response_payload(self, register):
        """Verify exist of payload in response."""
        response = register.post_register()
        assert response.json()

    def test_payload_type_validation(self, register):
        """Verify values type in response."""
        response = register.post_register()
        model = register.get_model(RegisterModel, response.json())
        assert isinstance(model, RegisterModel)

    @pytest.mark.parametrize("mail, pwd, name, exp",
                             empty_register_credentials)
    def test_empty_credentials_validation(self, register,
                                          mail, pwd, name, exp):
        """Verify response code with empty credentials."""
        register.data = register.setup_register_data(name, mail, pwd)
        response = register.post_register()
        assert response.status_code == exp

        with allure.step("Verify error 404 message"):
            payload = register.required_fields
            payload_model = register.get_model(MsgModel, payload)
            model = register.get_model(MsgModel, response.json())
            assert model == payload_model

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, register, method, exp):
        """Verify response code with invalid types of method."""
        response = register.send_requests(method, register.endpoint,
                                          None, register.data)
        assert response.status_code == exp
        register.attach_response(response.text)

    @pytest.mark.parametrize("data, exp", invalid_data)
    def test_invalid_data(self, register, data, exp):
        """Verify response code with invalid type of body."""
        register.data = data
        response = register.send_requests('post',
                                          register.endpoint,
                                          None,
                                          register.data)
        assert response.status_code == exp
        register.attach_response(response.text)

        with allure.step("Verify error 404 message"):
            payload = register.required_fields
            payload_model = MsgModel(**payload)
            model = register.get_model(MsgModel, response.json())
            assert model == payload_model

    email_validation = invalid_email_format + valid_email_formats

    @pytest.mark.parametrize("name, mail, pwd, exp", email_validation)
    def test_email_validation(self, register, name, mail, pwd, exp):
        """Verify response code with different email."""
        register.data = register.setup_register_data(name, mail, pwd)
        response = register.post_register()
        assert response.status_code == exp

    @pytest.mark.parametrize("name, mail, pwd, exp", password_validation)
    def test_password_validation(self, register, name, mail, pwd, exp):
        """Verify response code with different password length."""
        register.data = register.setup_register_data(name, mail, pwd)
        response = register.post_register()
        assert response.status_code == exp

    @pytest.mark.parametrize("name, mail, pwd, exp", name_validation)
    def test_name_validation(self, register, name, mail, pwd, exp):
        """Verify response code with different name."""
        register.data = register.setup_register_data(name, mail, pwd)
        response = register.post_register()
        assert response.status_code == exp

    def test_register_exist_user(self, register):
        """Verify response code with exist user registration."""
        response = register.post_register()
        assert response.status_code == 200

        with allure.step("Try register exist user"):
            response = register.post_register()
            assert response.status_code == 403

        with allure.step("Verify error 403 message"):
            payload = register.exist_user
            ExistUser = MsgModel
            payload_model = ExistUser(**payload)
            model = register.get_model(ExistUser, response.json())
            assert model == payload_model
