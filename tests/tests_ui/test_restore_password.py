"""
This module contains tests for Reset password features.
[tests DEFINITIONS]:
    Registered user credentials
    Not Registered user credential
    Main page
    Account Page
    Register page
    Forgot password page
    Login page
    Reset password page
    Access credentials to registered user email service server
    Access credentials to Not registered user email service server
[TESTS]:
    Verify access to Forgot-password page.
    Verify direct access to Forgot-password page.
    Verify sending restore password link with invalid email (Empty email).
    Verify sending restore password link with invalid email (Not registered email).
    Verify sending restore password link with invalid email (Email without domain part).
    Verify sending restore password link with invalid email (Email without username part).
    Verify sending restore password link with invalid email (Random string).
    Verify sending restore password link with invalid email (Random number).
    Verify redirection to Login page clicking Entry link.
    Verify redirection to Reset page.
    Verify redirection to pages using Header buttons (from Forgot to List of orders page).
    Verify redirection to pages using Header buttons (from Forgot to Main page).
    Verify redirection to pages using Header buttons (from Forgot to Login page).
    Verify redirection to Login page.
    Verify no redirection with invalid credential.
    (Error message presence if password < 6 chars) (Empty fields).
    Verify no redirection with invalid credential.
    (Error message presence if password < 6 chars) (No confirm code).
    Verify no redirection with invalid credential.
    (Error message presence if password < 6 chars) (Wrong confirm code).
    Verify user receive an email (Not registered email).
    Verify user receive an email (Registered email).
    Verify reset code structure in email.
    Verify user setup new password.
    Verify user sign in using new password.
    Verify redirection to pages using Header buttons (from Reset to List of orders page).
    Verify redirection to pages using Header buttons (from Reset to Main page).
    Verify redirection to pages using Header buttons (from Reset to Login page).
"""
# pylint: disable=W0613
import allure
import pytest
from playwright.sync_api import expect

from pages.forgot_page_class import FORGOT
from pages.login_page_class import LOGIN
from pages.main_page_class import MAIN
from pages.reset_page_class import RESET
from pages.account_page_class import ACCOUNT
from tests.utils import UTILS

from params_ui.registration_params import header_redirection
from params_ui.reset_password_params import email_validation, \
    email_send_code, reset_validation


@allure.step('Reset valid user password and login.')
def reset_and_login(forgot_page, mail, pwd):
    """Reset valid user password and login."""
    FORGOT.fill_forgot_field(forgot_page, mail)
    _, code = UTILS.mail_check(mail, pwd)
    RESET.set_restore_fields(forgot_page, pwd, code)
    LOGIN.set_login_fields(forgot_page, mail, pwd)


def test_forgot_access(forgot_page):
    """Verify access to Forgot-password page."""
    with allure.step("Verify redirection to Forgot-password page"):
        expect(forgot_page.locator(FORGOT.TOP_TITLE)).to_be_visible()


def test_forgot_direct_access(page_browser):
    """Verify direct access to Forgot-password page."""
    with allure.step("Set address to the browser"):
        page_browser.goto(FORGOT.FORGOT_LINK)

    with allure.step("Verify redirection to Forgot-password page"):
        expect(page_browser.locator(FORGOT.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("email, link", email_validation)
def test_forgot_email_validation(forgot_page, email, link):
    """Verify sending restore password link with invalid email."""
    FORGOT.fill_forgot_field(forgot_page, email)

    with allure.step("Verify user stays on the page"):
        expect(forgot_page).to_have_url(link)


def test_forgot_redirection_to_login_page(forgot_page):
    """Verify redirection to Login page clicking Entry link."""
    with allure.step("Click Entry link"):
        forgot_page.locator(FORGOT.ENTRY_LINK).click()

    with allure.step("Verify redirection to Login page"):
        expect(forgot_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


def test_forgot_redirection_to_reset_page(forgot_page):
    """Verify redirection to Reset page."""
    FORGOT.fill_forgot_field(forgot_page, FORGOT.registered_gmail)

    with allure.step("Verify redirection to Reset page"):
        expect(forgot_page.locator(RESET.SAVE_BTN)).to_be_visible()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_forgot_header_btns(login_page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click on button at Header"):
        login_page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(login_page.locator(exp)).to_be_visible()


def test_reset_redirection_to_login_page(forgot_page):
    """Verify redirection to Login page."""
    FORGOT.fill_forgot_field(forgot_page, FORGOT.registered_gmail)

    with allure.step("Click Entry link at the bottom of the page"):
        forgot_page.locator(RESET.ENTRY_LINK).click()

    with allure.step("Verify redirection to Login page"):
        expect(forgot_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("pwd, conf_code", reset_validation)
def test_reset_validation(forgot_page, pwd, conf_code):
    """Verify no redirection with invalid credential.
    (Error message presence if password < 6 chars)."""
    FORGOT.fill_forgot_field(forgot_page, FORGOT.registered_gmail)
    RESET.set_restore_fields(forgot_page, pwd, conf_code)

    with allure.step("Verify user stays on the page"):
        expect(forgot_page.locator(RESET.SAVE_BTN)).to_be_visible()

    if len(pwd) < 6 and pwd != "":
        with allure.step("Verify error shows up if password < 6"):
            expect(forgot_page.locator(RESET.PWD_ERROR_MSG)).to_be_visible()


@pytest.mark.parametrize('mail, pwd, exp, status',
                         email_send_code)
def test_reset_send_email(forgot_page, mail, pwd, exp, status):
    """Verify user receive an email."""
    FORGOT.fill_forgot_field(forgot_page, mail)

    with allure.step("Get mail address in email service"):
        address, _ = UTILS.mail_check(mail, pwd)

    with allure.step("Verify sender email address"):
        if status:
            assert address == exp
        else:
            assert address != exp


@pytest.mark.parametrize('mail, pwd, exp, status',
                         [email_send_code[1]])
def test_reset_code_structure(forgot_page, mail, pwd, exp, status):
    """Verify reset code structure in email."""
    FORGOT.fill_forgot_field(forgot_page, mail)

    with allure.step("Get mail address and code in email service"):
        address, code = UTILS.mail_check(mail, pwd)

    with allure.step("Verify sender email address and code structure"):
        if status:
            assert address == exp
            assert RESET.verify_confirmation_code(code)
        else:
            assert address != exp


@pytest.mark.parametrize('mail, pwd, exp, status',
                         [email_send_code[1]])
def test_reset_setup_new_pass(forgot_page, mail, pwd, exp, status):
    """Verify user setup new password."""
    FORGOT.fill_forgot_field(forgot_page, mail)
    _, code = UTILS.mail_check(mail, pwd)
    RESET.set_restore_fields(forgot_page, pwd, code)

    with allure.step("Verify redirection to Login page"):
        expect(forgot_page.locator(LOGIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('mail, pwd, exp, status',
                         [email_send_code[1]])
def test_reset_login_with_new_pwd(forgot_page, mail, pwd, exp, status):
    """Verify user login using new password."""
    reset_and_login(forgot_page, mail, pwd)

    with allure.step("Verify redirection to Main page"):
        expect(forgot_page.locator(MAIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('mail, pwd, exp, status',
                         [email_send_code[1]])
def test_reset_exist_password(forgot_page, mail, pwd, exp, status):
    """Verify reset password with exist password."""
    reset_and_login(forgot_page, mail, pwd)

    with allure.step("Verify redirection to Main page"):
        expect(forgot_page.locator(MAIN.TOP_TITLE)).to_be_visible()

    forgot_page.locator(MAIN.ACCOUNT_BTN).click()
    forgot_page.locator(ACCOUNT.LOGOUT_LINK).click()
    forgot_page.locator(LOGIN.RESTORE_PDW_LINK).click()

    reset_and_login(forgot_page, mail, pwd)

    with allure.step("Verify redirection to Main page"):
        expect(forgot_page.locator(MAIN.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_reset_header_btns(login_page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    FORGOT.fill_forgot_field(login_page, FORGOT.registered_gmail)

    with allure.step("Verify redirection to Reset page"):
        expect(login_page.locator(RESET.SAVE_BTN)).to_be_visible()

    with allure.step("Click on button at Header"):
        login_page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(login_page.locator(exp)).to_be_visible()
