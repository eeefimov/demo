"""Params for Login page."""
import pytest
from faker import Faker

from tests.settings import user_email
from pages.login_page_class import Login
from pages.registration_page_class import Register
from pages.forgot_page_class import Forgot
from pages.orders_page_class import Orders
from pages.main_page_class import Main

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
    pytest.param(Login.REGISTRATION_LINK,
                 Register.TOP_TITLE,
                 id='Redirection to Register page'),
    pytest.param(Login.RESTORE_PDW_LINK,
                 Forgot.TOP_TITLE,
                 id='Redirection to Forgot password page')
]

# Validation Header buttons.
header_redirection = [
    pytest.param(Login.LIST_OF_ORDERS_BTN,
                 Orders.TOP_TITLE,
                 id='Redirection to List of orders page'
                 ),
    pytest.param(Login.CONSTRUCTOR_BTN,
                 Main.TOP_TITLE,
                 id='Redirection to Main page'
                 )
]
