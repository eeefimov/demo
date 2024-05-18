"""
[FEATURES]:
    Check and setup token for authorization header.
    Setup response model.
    Return authenticated headers with the provided token.
    Load data from a JSON file and attach it to the Allure report.
    Send different types of requests.
    Attach api response to the Allure report.
    Attach request information to the Allure report.
    Send GET request.
"""
import os
import json
import allure
import requests
from pydantic import ValidationError
from faker import Faker
from tests.utils import UTILS
from api.endpoints import ENDPOINTS
fake = Faker()


class BASEAPI:
    """Base api class."""
    def __init__(self, endpoints=None):
        """Initialize the BASEAPI class with optional endpoints."""
        self.endpoints = endpoints if endpoints is not None else ENDPOINTS()
        self.data = None
        self.access_token = None
        self.header = None

    @staticmethod
    @allure.step('Check if Header for authorization and setup token')
    def setup_headers(headers, register):
        """Check and setup token for authorization header."""
        if 'Authorization' in headers:
            if headers['Authorization'] == 'empty':
                headers['Authorization'] = f'{register.access_token}'
        return headers

    @staticmethod
    @allure.step("Setup response model")
    def get_model(model, input_data):
        """Setup response model."""
        try:
            return model(**input_data)
        except ValidationError as e:
            return e.json()

    @staticmethod
    @allure.step('Setup Header with user token')
    def header_auth(token: str) -> dict:
        """Return authenticated headers with the provided token."""
        return {
            'Authorization': f'{token}'
        }

    @staticmethod
    @allure.step("Load data_models from json file")
    def load_data_from_file(filename: str):
        """Load data from a JSON file
        and attach it to the Allure report."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir,
                                      "..", "data_models",
                                      f"{filename}")
        BASEAPI.attach_response(UTILS.load_file(json_file_path))
        return UTILS.load_file(json_file_path)

    @staticmethod
    def send_requests(method: str, endpoint: str, header, payload):
        """Send different types of requests."""
        with allure.step(f"Send {method} requests"):
            try:
                if method == "get":
                    response = requests.get(endpoint, headers=header,
                                            data=payload, timeout=10)
                elif method == "post":
                    response = requests.post(endpoint, headers=header,
                                             data=payload, timeout=10)
                elif method == "put":
                    response = requests.put(endpoint, headers=header,
                                            data=payload, timeout=10)
                elif method == "patch":
                    response = requests.patch(endpoint, headers=header,
                                              data=payload, timeout=10)
                elif method == "delete":
                    response = requests.delete(endpoint, headers=header,
                                               data=payload, timeout=10)

                BASEAPI.attach_request_info(method, endpoint, header, payload)
                return response

            except requests.exceptions.RequestException as e:
                print(f"Error sending {method} request: {e}")
                raise e

    @staticmethod
    def attach_response(response):
        """Attach api response to the Allure report."""
        if isinstance(response, str):
            allure.attach(body=response,
                          name="api Response",
                          attachment_type=allure.attachment_type.TEXT)

        elif isinstance(response, dict):
            response_json = json.dumps(response)
            allure.attach(body=response_json,
                          name="api Response",
                          attachment_type=allure.attachment_type.JSON)

        elif response.json():
            response_json = response.json()
            response = json.dumps(response_json, indent=4)
            allure.attach(body=response,
                          name="api Response",
                          attachment_type=allure.attachment_type.JSON)

    @staticmethod
    def attach_request_info(method, endpoint, header, payload):
        """Attach request information to the Allure report."""
        request_info = {
            'method': method,
            'endpoint': endpoint,
            'header': header,
            'data_models': payload
        }
        with open('request_info.txt', 'w', encoding='utf-8') as file:
            for key, value in request_info.items():
                file.write(f"{key} = {value}\n")

        allure.attach.file('request_info.txt',
                           name='Request Info',
                           attachment_type=allure.attachment_type.TEXT)

    @allure.step('Send GET request')
    def get_request(self, endpoint):
        """Send GET request."""
        self.attach_response(self.header)
        response = requests.get(url=endpoint,
                                params=None,
                                data=None,
                                headers=self.header,
                                timeout=10)
        if response.status_code == 200:
            self.attach_response(response.json())

        return response
