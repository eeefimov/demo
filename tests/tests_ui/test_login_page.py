"""
This module contains tests for Login page.

[tests DEFINITIONS]:
    Registered user credentials
    Not Registered user credential
    Main page
    Login page
    Register page
    Forgot password page
    List of orders page
[TESTS]:
    Verify access to Login page.
    Verify direct access to Login page.
    Verify sign in with empty user credentials.
    Verify sign in with Not registered email, empty password.
    Verify sign in with Not registered email, with password < 6.
    Verify sign in with Not registered email, with password = 6.
    Verify sign in with Valid email, invalid password = 6.
    Verify sign in with Valid email, invalid password < 6.
    Verify sign in with valid user credentials.
    Verify redirection to pages using Header buttons (Register page).
    Verify redirection to pages using Header buttons (Forgot password page).
    Verify redirection to pages using Header buttons (List of orders page).
    Verify redirection to pages using Header buttons (Main page).
"""
import time
import pytest
import allure
from playwright.sync_api import expect

from pages.login_page_class import Login
from pages.main_page_class import Main

from params_ui.login_params import login_validation, \
    login_redirections, header_redirection


def test_login_access(login_page):
    """Verify access to Login page."""
    with allure.step('Verify redirection to Login page'):
        expect(login_page.locator(Login.TOP_TITLE)).to_be_visible()


def test_login_direct_access(page_browser):
    """Verify direct access to Login page."""
    with allure.step("Set the address to the browser"):
        page_browser.goto(Login.LOGIN_LINK)

    with allure.step('Verify redirection to Login page'):
        expect(page_browser.locator(Login.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize("email_val, pwd_val", login_validation)
def test_login_validation(login_page, email_val, pwd_val):
    """Verify sign in with different credentials."""
    Login.set_login_fields(login_page, email_val, pwd_val)
    time.sleep(1)

    with allure.step('Click on Entry button'):
        login_page.locator(Login.ENTRY_BTN).click()

    if 1 < len(pwd_val) < 6:
        with allure.step("Verify password error shows up"):
            expect(login_page.locator(Login.PWD_ERROR)).to_be_visible()

    if email_val != Login.mail and pwd_val != Login.pwd:
        with allure.step("Verify the user stays at Login page"):
            expect(login_page.locator(Login.TOP_TITLE)).to_be_visible()


def test_login_valid(login_page):
    """Verify sign in with valid user credentials."""
    Login.user_sign_in(login_page)

    with allure.step("Verify redirection to Main page"):
        expect(login_page.locator(Main.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('link, title_txt', login_redirections)
def test_login_redirection(login_page, link, title_txt):
    """Verify redirection to Register and Forgot-password pages."""
    with allure.step('Click on the link at the top of Login form'):
        login_page.locator(link).click()

    with allure.step(f"Verify redirection to {link} page"):
        expect(login_page.locator(title_txt)).to_be_visible()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_login_header_btns(login_page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click on button at Header"):
        login_page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(login_page.locator(exp)).to_be_visible()
