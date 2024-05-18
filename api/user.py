# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-function-args
"""
Class for handling USERs api requests.
[FEATURES]:
    Set user registration data.
    Send POST request register new user.
    Send POST request login user.
    Setup request reset user password.
    Send GET request user with provided token.
    Generate new user data for PATCH request.
    Send PATCH request.
    Send DELETE user request.
    Setup logout data.
    Send POST request logout.
"""
import allure
import requests
from faker import Faker
from api.base import BASEAPI

fake = Faker()


class USER(BASEAPI):
    """USER class for handling api requests."""
    def __init__(self):
        super().__init__()
        self.endpoint = self.endpoints.register
        self.required_fields = {
            "success": False,
            "message": "Email, password and name are required fields"
        }
        self.exist_user = {
            "success": False,
            "message": "User already exists"
        }
        self.authorisation = {
            'success': False,
            'message': 'You should be authorised'
        }
        self.exis_email = {
            "success": False,
            "message": "User with such email already exists"
        }
        self.reset_sent = {
            "success": True,
            "message": "Reset email sent"
        }
        self.successful_logout = {
            'success': True,
            'message': 'Successful logout'
        }
        self.toke_required = {
            'success': False,
            'message': 'Token required'
        }

    @allure.step('Set user registration data_models')
    def setup_register_data(self, name, mail, pwd):
        """Set user registration data."""
        return {
            'name': name,
            'email': mail,
            'password': pwd
        }

    @allure.step("Send POST register request")
    def post_register(self):
        """Send POST request register new user."""
        url = self.endpoint
        response = requests.post(url, json=self.data,
                                 timeout=10)

        if response.status_code == 200:
            self.access_token = response.json().get("accessToken")
            self.attach_request_info('POST', url, None, self.data)

        if response.status_code != 500:
            self.attach_response(response)
        return response

    @allure.step("Send POST login request")
    def post_login(self, data):
        """Send POST request login user."""
        url = self.endpoints.login
        response = requests.post(url, json=data, timeout=10)
        self.attach_request_info('POST', url, None, self.data)

        if response.status_code == 200:
            self.attach_response(response)
        return response

    @allure.step('Setup reset request')
    def setup_reset(self, reset):
        """Setup request reset user password."""
        reset.post_register()
        reset.endpoint = self.endpoints.reset_pwd
        reset.data = {
            "email": f"{reset.data['email']}"}
        return reset

    @allure.step("Send GET user request")
    def get_user(self):
        """Send GET request user with provided token."""
        url = self.endpoints.user
        response = requests.get(url, headers=self.header,
                                json=None, timeout=10)
        self.attach_request_info('GET', url, self.header, None)
        self.attach_response(response)
        return response

    @allure.step('Setup new user data')
    def new_user_data(self, value):
        """Generate new user data."""
        if value == 'email':
            new_data = {'email': f"new{fake.email()}"}
        elif value == 'name':
            new_data = {'name': f"new{fake.user_name()}"}
        elif value == 'pwd':
            new_data = {'password': f"new{fake.password()}"}
        return new_data

    @allure.step("Send PATCH user request")
    def patch_user(self, new_data):
        """Send PATCH request."""
        url = self.endpoints.user
        response = requests.patch(url, headers=self.header,
                                  data=new_data, timeout=10)
        self.attach_request_info('PATCH', url, self.header, self.data)
        self.attach_response(response)
        return response

    @allure.step("Send DELETE request")
    def delete_user(self, access_token):
        """Send DELETE user request."""
        url = self.endpoints.user
        header = self.header_auth(access_token)
        response = requests.delete(url, headers=header, timeout=10)
        self.attach_request_info('DELETE', url, header, None)
        print('User was deleted')
        return response

    @allure.step("Setup logout data")
    def setup_logout(self, data):
        """Setup logout data."""
        self.data = {
            'token': data
        }

    @allure.step("Send POST logout request")
    def post_logout(self, data):
        """Send POST request logout."""
        self.setup_logout(data)
        url = self.endpoints.logout
        response = requests.post(url, json=self.data,
                                 timeout=10)
        self.attach_request_info('POST', self.endpoint,
                                 None, self.data)
        if response.status_code == 200:
            self.attach_response(response)
        return response
