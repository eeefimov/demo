"""Params for Registration page."""
import pytest
from faker import Faker

from pages.registration_page_class import REGISTER
from pages.main_page_class import MAIN
from pages.orders_page_class import ORDERS
from pages.login_page_class import LOGIN

fake = Faker()
special = fake.random_element(elements=(
    '!', '@', '#', '$', '%', '^', '&', '*')) * 10

# Empty validation.
empty_validation = [
    pytest.param("", "", "",
                 id='Empty user credentials'),
    pytest.param("", fake.email(), fake.password()[:6],
                 id='Empty post_login'),
    pytest.param(fake.user_name(), "", fake.password()[:6],
                 id='Empty email'),
    pytest.param(fake.user_name(), fake.email(), "",
                 id='Empty password')
]

# Password length validation.
password_validation = [
    pytest.param(fake.user_name(),
                 fake.email(),
                 fake.password(length=5),
                 id='Password < 6'),
    pytest.param(fake.user_name(),
                 fake.email(),
                 fake.password(length=100),
                 id='Password 100'),
    pytest.param(fake.user_name(),
                 fake.email(),
                 fake.password(length=10),
                 id='Password 10')
]

# Login validation.
name_validation = [
    pytest.param(fake.name()[0],
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with 1 char'),
    pytest.param(str(fake.random_number(digits=10)),
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with 10 digits'),
    pytest.param(special,
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with special chars'),
    pytest.param(fake.text(max_nb_chars=100),
                 fake.email(), fake.password()[:6],
                 id='User post_login with 100 char'),
    pytest.param(" ".join(fake.words(2)),
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with 2 strings'),
    pytest.param(" ".join(fake.words(3)),
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with 3 strings'),
    pytest.param(" " + fake.word(),
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with front space string'),
    pytest.param(fake.word() + " ",
                 fake.email(),
                 fake.password()[:6],
                 id='User post_login with back space string')
]

# Invalid email format validation.
email_format_validation = [
    pytest.param(fake.user_name(),
                 fake.email().replace('@', 'a'),
                 fake.password()[:6],
                 id='Email without "@"'),
    pytest.param(fake.user_name(),
                 fake.email().split('@', 1)[0] + '@',
                 fake.password()[:6],
                 id='Email without domain part'),
    pytest.param(fake.user_name(),
                 '@' + fake.email().split('@', 1)[1],
                 fake.password()[:6],
                 id='Email without username part'),
]

# Different email format validation.
email_validation = [
    # name.name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}."
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with one dot in username'),
    # name.name.name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}."
                 f"{fake.last_name()}."
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with two dots in username'),
    # name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}_"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with underscore in username'),
    # name_name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}_"
                 f"{fake.last_name()}_"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with three underscores in username'),
    # name-name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with dash in username'),
    # name-name-name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}-"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with three dashes in username'),
    # name-name.name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}."
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 id='Email with dash and dot in username'),
]

# Valid credentials.
valid_user_credentials = [
    pytest.param(fake.first_name(),
                 fake.email(),
                 fake.password()[:10],
                 id="Valid user credentials")
]

# Validation Header buttons.
header_redirection = [
    pytest.param(REGISTER.LIST_OF_ORDERS_BTN,
                 ORDERS.TOP_TITLE,
                 id='Redirection to List of orders page'
                 ),
    pytest.param(REGISTER.CONSTRUCTOR_BTN,
                 MAIN.TOP_TITLE,
                 id='Redirection to Main page'
                 ),
    pytest.param(REGISTER.ACCOUNT_BTN,
                 LOGIN.TOP_TITLE,
                 id='Redirection to Login page'
                 )
]
