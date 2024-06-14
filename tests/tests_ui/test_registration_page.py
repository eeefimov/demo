"""
This module contains tests for Registration page.

[tests DEFINITIONS]:
    Registered user credentials
    Not Registered user credential
    Main page
    Login page
    Registration page
    List of orders page
[TESTS]:
    Verify access to Register page.
    Verify direct access to Register page.
    Verify registration with Empty user credentials.
    Verify registration with Empty login.
    Verify registration with Empty email.
    Verify registration with Empty password.
    Verify presence of error message if password less than 6 chars.
    Verify registration with a different password length (< 6).
    Verify registration with a different password length (100).
    Verify registration with a different password length (10).
    Verify registration with a different invalid name values (1 char).
    Verify registration with a different invalid name values (10 digits).
    Verify registration with a different invalid name values (special chars).
    Verify registration with a different invalid name values (100 char).
    Verify registration with a different invalid name values (2 strings).
    Verify registration with a different invalid name values (3 strings).
    Verify registration with a different invalid name values
        (front space string).
    Verify registration with a different invalid name values
        (back space string).
    Verify registration with a different invalid email format (without "@").
    Verify registration with a different invalid email format
        (without domain part).
    Verify registration with a different invalid email format
        (without username part).
    Verify registration with a different email format (one dot in username).
    Verify registration with a different email format (two dots in username).
    Verify registration with a different email format (underscore in username).
    Verify registration with a different email format
        (three underscores in username).
    Verify registration with a different email format (dash in username).
    Verify registration with a different email format
        (three dashes in username).
    Verify registration with a different email format
        (dash and dot in username).
    Verify presence of the error message if invalid email format.
    Verify registration with valid user credentials.
    Verify presence of the error message if using exist user credentials.
    Verify LogIn of new registered user.
    Verify redirection to Login page click Entry link.
    Verify redirection to pages using Header buttons (List of orders page).
    Verify redirection to pages using Header buttons (Main page).
    Verify redirection to pages using Header buttons (Login page).
"""
import pytest
import allure
from playwright.sync_api import expect

from params_ui.registration_params import empty_validation, \
    password_validation, name_validation, email_format_validation, \
    email_validation, valid_user_credentials, header_redirection

from pages.registration_page_class import REGISTER
from pages.login_page_class import LOGIN
from pages.main_page_class import MAIN


def test_register_access(register_page):
    """Verify access to Register page."""
    with allure.step("Verify redirection to Registration page"):
        expect(register_page.locator(REGISTER.TOP_TITLE)).to_be_visible()


def test_register_direct_access(page):
    """Verify direct access to Register page."""
    with allure.step("Go to site"):
        page.goto(REGISTER.REGISTER_LINK)

    with allure.step("Verify redirection to Registration page"):
        expect(page.locator(REGISTER.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", empty_validation)
def test_register_validation_empty(register_page, name, mail, pwd):
    """Verify registration with empty credentials."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("User stays at Registration page."):
        expect(register_page.locator(LOGIN.TOP_TITLE)).not_to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", [password_validation[0]])
def test_register_password_error_msg(register_page, name, mail, pwd):
    """Verify presence of error message if password less than 6 chars."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("Verify that Password Error message shows up"):
        expect(register_page.locator(REGISTER.PWD_ERROR)).to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", password_validation)
def test_register_password_validation(register_page, name, mail, pwd):
    """Verify registration with a different password length."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    if len(pwd) < 6:
        with allure.step("Click Registration button (Double check)"):
            register_page.locator(REGISTER.REGISTRATION_BTN).click()

        with allure.step("User not redirects to Login page."):
            expect(register_page.locator(LOGIN.TOP_TITLE)).not_to_be_visible()
    else:
        with allure.step("User redirects to Login page."):
            expect(register_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", name_validation)
def test_register_name_validation(register_page, name, mail, pwd):
    """Verify registration with a different invalid name values."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("User stays at Registration page."):
        expect(register_page.locator(LOGIN.TOP_TITLE)).not_to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", email_format_validation)
def test_register_email_invalid_format_validation(register_page, name,
                                                  mail, pwd):
    """Verify registration with a different invalid email format."""
    with allure.step("Set all Registration fields"):
        REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("User redirects to Login page."):
        expect(register_page.locator(LOGIN.TOP_TITLE)).not_to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", email_validation)
def test_register_email_validation(register_page, name, mail, pwd):
    """Verify registration with a different email format."""
    with allure.step("Set all Registration fields"):
        REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("User redirects to Login page."):
        expect(register_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("name, mail, pwd", [email_format_validation[0]])
def test_register_email_error_txt(register_page, name, mail, pwd):
    """Verify presence of the error message if invalid email format."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("Verify that Email Error message shows up"):
        expect(
            register_page.locator(REGISTER.MAIL_ERROR)).to_be_visible()

    with allure.step("Verify text of Email Error"):
        expect(register_page.locator(
                REGISTER.MAIL_ERROR)).to_contain_text('Некорректный email')


@pytest.mark.parametrize("name, mail, pwd", valid_user_credentials)
def test_register_valid_user(register_page, name, mail, pwd):
    """Verify registration with valid user credentials."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)

    with allure.step("User redirects to Login page."):
        expect(register_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


def test_register_exist_user(register_page):
    """Verify presence of the error message
    if using exist user credentials."""
    REGISTER.set_register_fields(register_page,
                                 REGISTER.name,
                                 REGISTER.mail,
                                 REGISTER.pwd)

    with allure.step("Verify that User Error message shows up"):
        expect(register_page.locator(REGISTER.USER_ERROR)).to_be_visible()

    with allure.step("Verify text of User Error message"):
        expect(register_page.locator(REGISTER.USER_ERROR)).to_contain_text(
            'Такой пользователь уже существует')


@pytest.mark.parametrize("name, mail, pwd", valid_user_credentials)
def test_register_login_new_registered_user(register_page, name, mail, pwd):
    """Verify LogIn of new registered user."""
    REGISTER.set_register_fields(register_page, name, mail, pwd)
    LOGIN.set_login_fields(register_page, mail, pwd)

    with allure.step("Verify redirection to Main Page"):
        expect(register_page.locator(MAIN.TOP_TITLE)).to_be_visible()


def test_register_redirection_to_login_page(register_page):
    """Verify redirection to Login page click Entry link."""
    with allure.step("Click Entry link"):
        register_page.locator(REGISTER.ENTRY_LINK).click()

    with allure.step("Verify redirection to Login Page"):
        expect(register_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_register_header_btns(login_page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click on button at Header"):
        login_page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(login_page.locator(exp)).to_be_visible()
