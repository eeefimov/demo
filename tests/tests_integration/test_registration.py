"""
[tests FEATURES]:
    Verify UI SignIn with valid api registered user credentials.
    Verify UI SignIn with different API password registration (Password < 6).
    Verify UI SignIn with different API password registration (Password 100).
"""
import time
import allure
import pytest
from playwright.sync_api import expect
from pages.main_page_class import Main
from pages.login_page_class import Login
from params_api.api_register_params import password_validation


def test_valid_credentials(login_page, register):
    """Verify UI SignIn with valid api registered user credentials."""
    register.post_register()
    mail = register.data['email']
    pwd = register.data['password']
    Login.set_login_fields(login_page, mail, pwd)
    expect(login_page.locator(Main.TOP_TITLE)).to_be_visible()

# pylint: disable=unused-argument
# pylint: disable=too-many-arguments


@pytest.mark.parametrize("name, mail, pwd, exp", password_validation)
def test_password_validation(login_page, register, name, mail, pwd, exp):
    """Verify UI SignIn with different API password registration."""
    register.data = register.setup_register_data(name, mail, pwd)
    register.post_register()
    mail = register.data['email']
    pwd = register.data['password']
    Login.set_login_fields(login_page, mail, pwd)
    if len(pwd) < 6:
        with allure.step('Double check SignIn with invalid pwd'):
            login_page.locator(Login.ENTRY_BTN).click()
            time.sleep(2)
            expect(login_page.locator(Main.TOP_TITLE)).not_to_be_visible()
    else:
        expect(login_page.locator(Main.TOP_TITLE)).to_be_visible()
