"""Params for users api"""
import pytest
from faker import Faker

fake = Faker()

# invalid token validation
invalid_token = [
    pytest.param("", 401, id="Empty token"),
    pytest.param(fake.password(), 401, id="Invalid token")
]

# invalid methods validation
invalid_methods = [
    pytest.param('post', 403, id='POST'),
    pytest.param('put', 404, id='PUT')
]
# valid patch values
patch_valid = [
    pytest.param('email', 200, id='PATCH email'),
    pytest.param('name', 200, id='PATCH name'),
    pytest.param('pwd', 200, id='PATCH password')
]
