"""Parameters for Reset and Forgot password page."""
import pytest
from faker import Faker

from tests.settings import gmail_password_registered, \
    gmail_user_registered, gmail_password_not_registered, \
    gmail_user_not_registered

fake = Faker()

FORGOT_LINK = 'https://stellarburgers.nomoreparties.site/forgot-password'

#   Email validation.
email_validation = [
    pytest.param("",
                 FORGOT_LINK,
                 id="Empty email"),
    pytest.param(fake.email(),
                 FORGOT_LINK,
                 id='Not registered email'),
    pytest.param(fake.email().split('@', 1)[0] + '@',
                 FORGOT_LINK,
                 id='Email without domain part'),
    pytest.param('@' + fake.email().split('@', 1)[1],
                 FORGOT_LINK,
                 id='Email without username part'),
    pytest.param(fake.text(),
                 FORGOT_LINK,
                 id='Random string'),
    pytest.param(str(fake.random_number(digits=10)),
                 FORGOT_LINK,
                 id='Random number'),
]

# Reset validation invalid.
reset_validation = [
    pytest.param("",
                 "",
                 id="Empty fields"),
    pytest.param(fake.password()[:5],
                 "",
                 id="PWD < 6"),
    pytest.param(fake.password()[:6],
                 "",
                 id="No confirm code"),
    pytest.param(fake.password()[:6],
                 fake.password(),
                 id="Wrong confirm code")
]

# Send confirmation code email validation.
email_send_code = [
    pytest.param(gmail_user_not_registered,
                 gmail_password_not_registered,
                 'Praktikum <no.more.parties@yandex.ru>',
                 False,
                 id='Not registered email'),
    pytest.param(gmail_user_registered,
                 gmail_password_registered,
                 'Praktikum <no.more.parties@yandex.ru>',
                 True,
                 id='Registered email'),
]
