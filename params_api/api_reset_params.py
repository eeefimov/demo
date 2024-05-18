"""Params for reset api"""
import pytest

from tests.settings import gmail_password_registered, \
    gmail_user_registered, gmail_password_not_registered, \
    gmail_user_not_registered

# send_code_email_validation
email_send_code = [
    pytest.param(gmail_user_not_registered,
                 gmail_password_not_registered,
                 id='Not registered email'),
    pytest.param(gmail_user_registered,
                 gmail_password_registered,
                 id='Registered email'),
]
