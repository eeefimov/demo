# pylint: disable=duplicate-code
# registration invalid methods:
"""Params for register api"""
import pytest
from faker import Faker

fake = Faker()

special = fake.random_element(elements=(
    '!', '@', '#', '$', '%', '^', '&', '*')) * 10


empty_register_credentials = [
    pytest.param("",
                 fake.password(),
                 fake.user_name(),
                 400,
                 id="No email"),
    pytest.param(fake.email(),
                 "",
                 fake.user_name(),
                 400,
                 id="No password"),
    pytest.param(fake.email(),
                 fake.password(),
                 "",
                 400,
                 id="No name"),
    pytest.param("",
                 "",
                 "",
                 400,
                 id="All empty")
]

invalid_methods = [
    pytest.param('get',
                 404,
                 id='GET'),
    pytest.param('put',
                 404,
                 id='PUT'),
    pytest.param('patch',
                 404,
                 id='PATCH')
]

# Invalid data_models
invalid_data = [
    pytest.param(None,
                 400,
                 id='None data_models'),
    pytest.param(
        {
            fake.password(): fake.password(),
            fake.password(): fake.password(),
            fake.password(): fake.password(),
        },
        400,
        id="Invalid data_models")
]

# Invalid email format validation.
invalid_email_format = [
    pytest.param(fake.user_name(),
                 fake.email().replace('@', 'a'),
                 fake.password()[:6],
                 400,
                 id='Email without "@"'),
    pytest.param(fake.user_name(),
                 fake.email().split('@', 1)[0] + '@',
                 fake.password()[:6],
                 400,
                 id='Email without domain part'),
    pytest.param(fake.user_name(),
                 '@' + fake.email().split('@', 1)[1],
                 fake.password()[:6],
                 400,
                 id='Email without username part'),
    pytest.param(fake.user_name(),
                 fake.random_number(digits=7),
                 fake.password()[:6],
                 400,
                 id="Integer in email")
]

# Valid email format validation.
valid_email_formats = [
    # name.name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}."
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with one dot in username'),
    # name.name.name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}."
                 f"{fake.last_name()}."
                 f"{fake.first_name()}"
                 f"@{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with two dots in username'),
    # name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}_"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with underscore in username'),
    # name_name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}_"
                 f"{fake.last_name()}_"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with three underscores in username'),
    # name-name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with dash in username'),
    # name-name-name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}-"
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with three dashes in username'),
    # name-name.name_name@domain.com
    pytest.param(fake.user_name(),
                 f"{fake.first_name()}-"
                 f"{fake.last_name()}."
                 f"{fake.last_name()}@"
                 f"{fake.domain_name()}",
                 fake.password()[:6],
                 200,
                 id='Email with dash and dot in username'),
]

# Password length validation.
password_validation = [
    pytest.param(fake.user_name(),
                 fake.email(),
                 fake.password()[:5],
                 400,
                 id='Password < 6'),
    pytest.param(fake.user_name(),
                 fake.email(),
                 fake.password(length=100),
                 200,
                 id='Password 100'),
]

# Name validation.
name_validation = [
    pytest.param(fake.name()[0],
                 fake.email(),
                 fake.password()[:6],
                 200,
                 id='User name with 1 char'),
    pytest.param(str(fake.random_number(digits=10)),
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with 10 digits'),
    pytest.param(special,
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with special chars'),
    pytest.param(fake.text(max_nb_chars=100),
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with 100 char'),
    pytest.param(" ".join(fake.words(2)),
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with 2 strings'),
    pytest.param(" ".join(fake.words(3)),
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with 3 strings'),
    pytest.param(" " + fake.word(),
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with front space string'),
    pytest.param(fake.word() + " ",
                 fake.email(),
                 fake.password()[:6],
                 400,
                 id='User name with back space string')
]
