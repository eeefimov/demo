"""Params for Login page."""
import pytest
from faker import Faker

from tests.settings import user_email
from pages.login_page_class import LOGIN
from pages.registration_page_class import REGISTER
from pages.forgot_page_class import FORGOT
from pages.orders_page_class import ORDERS
from pages.main_page_class import MAIN

fake = Faker()

# Login post_login validation.
login_validation = [
    pytest.param("",
                 "",
                 id='Empty user credentials'),
    pytest.param(fake.email(),
                 "",
                 id='Not registered email, empty password'),
    pytest.param(fake.email(),
                 fake.password()[:5],
                 id='Not registered email, with password < 6'),
    pytest.param(fake.email(),
                 fake.password()[:6],
                 id='Not registered email, with password = 6'),
    pytest.param(user_email,
                 fake.password()[:6],
                 id='Valid email, invalid password = 6'),
    pytest.param(user_email,
                 fake.password()[:5],
                 id='Valid email, invalid password < 6')
]

# Redirection to Register and Forgot pages.
login_redirections = [
    pytest.param(LOGIN.REGISTRATION_LINK,
                 REGISTER.TOP_TITLE,
                 id='Redirection to Register page'),
    pytest.param(LOGIN.RESTORE_PDW_LINK,
                 FORGOT.TOP_TITLE,
                 id='Redirection to Forgot password page')
]

# Validation Header buttons.
header_redirection = [
    pytest.param(LOGIN.LIST_OF_ORDERS_BTN,
                 ORDERS.TOP_TITLE,
                 id='Redirection to List of orders page'
                 ),
    pytest.param(LOGIN.CONSTRUCTOR_BTN,
                 MAIN.TOP_TITLE,
                 id='Redirection to Main page'
                 )
]
