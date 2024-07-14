"""
This module contains tests for Account page.

[tests DEFINITIONS]:
    Registered user credentials
    Main page
    Login page
    Account Page
    Order History page
    Order Modal window
[TESTS]:
    Verify registered user access to Account page.
    Verify presence of credentials in Account page fields.
    Verify redirection to Orders History page.
    Verify redirection to Profile page.
    Verify redirection from Account page after logout.
    Verify user has no access to Account page after logout.
    Verify redirection to pages using Header buttons (List of orders page).
    Verify redirection to pages using Header buttons (Account page).
    Verify presence of new order in Order History page.
    Verify presence of new order price in Order History page
    with a single bun.
    Verify presence of new order price in Order History page
    with bun + single ingredient.
    Verify presence of new order price in Order History page
    with bun + multiple ingredients.
    Verify presence of new order icons in Order History page
    with a single bun.
    Verify presence of new order icons in Order History page
    with bun + single ingredient.
    Verify presence of new order icons in Order History page
    with bun + multiple ingredients.
    Verify presence of new order icons in Order History page
    without bun, random ingredient number.
    Verify shows up Modal window clicking order item in
    Order History page.
"""
import pytest
import random
import allure
from playwright.sync_api import expect

from pages.account_page_class import Account
from pages.login_page_class import Login
from pages.main_page_class import Main

from params_ui.login_params import header_redirection
from params_ui.main_page_params import different_orders


def test_account_access(account_page):
    """Verify registered user access to Account page."""
    with allure.step("Verify redirection to Account page"):
        expect(account_page.locator(Account.PROFILE_LINK)).to_be_visible()


def test_account_credentials(account_page):
    """Verify presence of credentials in Account page fields."""
    with allure.step("Verify presence of use credentials"):
        expect(account_page.locator(
            Account.LOGIN_TITLE)).to_have_value(Account.name)
        expect(account_page.locator(
            Account.EMAIL_TITLE)).to_have_value(Account.mail)


def test_account_history_redirection(account_page):
    """Verify redirection to Orders History page."""
    Account.go_to_account_history(account_page)

    with allure.step("Verify redirection to Orders History page"):
        expect(account_page).to_have_url(Account.link)


def test_account_profile_redirection(account_page):
    """Verify redirection to Profile page."""
    Account.go_to_account_history(account_page)

    with allure.step("Click Profile link"):
        account_page.locator(Account.PROFILE_LINK).click()

    with allure.step("Verify redirection to Profile page"):
        expect(account_page.locator(Account.SAVE_BTN)).to_be_visible()


def test_account_logout(account_page):
    """Verify redirection from Account page after logout."""
    with allure.step("Click Logout link"):
        account_page.locator(Account.LOGOUT_LINK).click()

    with allure.step("Verify redirection to Login page"):
        expect(account_page.locator(Login.TOP_TITLE)).to_be_visible()


def test_account_no_access(account_page):
    """Verify user has no access to Account page after logout."""
    with allure.step("Click Logout link"):
        account_page.locator(Account.LOGOUT_LINK).click()

    with allure.step("Click Account on Header"):
        account_page.locator(Login.ACCOUNT_BTN).click()

    with allure.step("Verify user stays at Login page"):
        expect(account_page.locator(Login.TOP_TITLE)).to_be_visible()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_account_header_btns(account_page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click button on Header"):
        account_page.locator(btn).click()

    with allure.step("Verify redirection to Header button page"):
        expect(account_page.locator(exp)).to_be_visible()


def test_account_history_new_order_item(page):
    """Verify presence of new order in Order History page."""
    Main.make_order(page)
    order_number = Main.get_order_number(page)
    Main.close_modal_and_redirects(page, Main.ACCOUNT_BTN)
    Account.go_to_account_history(page)

    with allure.step("Verify presence of new order"):
        assert order_number == Account.get_order_number(page, Account.counter)


@allure.issue("Invalid calculation price for orders with Buns")
def test_account_history_order_price(page):
    """Verify price of the new order in Order History page."""
    Login.user_sign_in(page)
    Main.add_ingredients(page, True, 3)
    order_price = page.locator(Main.TOTAL_PRICE).inner_text()

    with allure.step("Click Order button"):
        page.locator(Main.BOTTOM_BTN).click()

    Main.close_modal_and_redirects(page, Main.ACCOUNT_BTN)
    Account.go_to_account_history(page)

    with allure.step("Verify correct new order price"):
        assert order_price == Account.get_order_price(page, Account.counter)


@allure.issue("The number of icons does not equal the number of ingredients in the order item.")
@pytest.mark.parametrize("bun, number", different_orders)
def test_account_history_ingredients_icons(page, bun, number):
    """Verify presence new order icons in Order History page."""
    # using the same params, do correction for orders.
    bun, number = Account.check_bun_ingredients(bun, number)

    Login.user_sign_in(page)
    Main.add_ingredients(page, bun, number)

    with allure.step("Click Order button"):
        page.locator(Main.BOTTOM_BTN).click()

    Main.close_modal_and_redirects(page, Main.ACCOUNT_BTN)
    Account.go_to_account_history(page)
    icons = page.locator(
        Account.get_order_icons_locator(Account.counter)).count()

    with allure.step("Verify number of ingredient icons "
                     "according to added ingredients"):
        if number >= 5:
            assert icons == 5
        else:
            assert icons == number + 1


def test_account_history_order_window(account_page):
    """Verify shows up Modal window
    clicking order item in Order History page
    (Precondition: User orders exist)."""
    Account.go_to_account_history(account_page)

    with allure.step("Click Last Order Item"):
        account_page.locator(Account.get_locator(
            Account.ORDER_ITEMS, Account.counter)).click()

    with allure.step("Verify Modal window shows up"):
        expect(account_page.locator(
            Account.ORDER_INFO_WNDW)).to_be_visible()
