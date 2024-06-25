"""
Description Account Class functions:
    Decorator for getting orders counter
    after user go to the Orders History page.
    Click Order History link at Account page."
    Redirects to Account page.
    Return text of new order number.
    Return icons locator in order item.
    Setup bun and ingredients to check icons in order history.
"""
import time
import allure
from pages.base_class import BaseClass
from pages.login_page_class import Login


class Account(BaseClass):
    """Class with functions for Account page feature."""
    link = 'https://stellarburgers.nomoreparties.site/account/order-history'

    PROFILE_LINK = "//a[contains(text(),'Профиль')]"
    LOGIN_TITLE = "(//input[contains(@class, 'input__textfield-disabled')])[1]"
    EMAIL_TITLE = "(//input[contains(@class, 'input__textfield-disabled')])[2]"

    ORDER_HISTORY_LINK = "//a[contains(text(),'История заказов')]"
    ORDER_ITEMS = "//li[contains(@class, 'mb-6')]"
    ORDER_ICONS_BOX = "//div[@class='OrderHistory_dataBox__1mkxK']"
    ORDER_ICONS = "//li[@class='OrderHistory_ingItem__24RJO']"
    ORDER_ITEMS_NUMBER = "//p[@class='text text_type_digits-default']"
    ORDER_ITEMS_PRICE = "//p[contains(@class, 'mr-2')]"
    ORDER_INFO_WNDW = "//div[contains(@class, 'Modal_orderBox')]"

    SAVE_BTN = "//button[contains(text(), 'Сохранить')]"
    LOGOUT_LINK = "//button[contains(text(), 'Выход')]"

    counter = None

    @staticmethod
    def get_counter(func):
        """Decorator for getting orders counter
        after user got to the Orders History page."""
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(2)
            Account.counter = args[0].locator(
                Account.ORDER_ITEMS_NUMBER).count()
        return wrapper

    @staticmethod
    @allure.step("Click Order History link")
    @get_counter
    def go_to_account_history(page: object) -> None:
        """Click Order History link at Account page."""
        page.locator(Account.ORDER_HISTORY_LINK).click()

    @staticmethod
    @allure.step("Click Account on Header")
    def go_to_account(page: object) -> None:
        """Redirects to Account page."""
        Login.user_sign_in(page)
        page.locator(Login.ACCOUNT_BTN).click()

    @staticmethod
    def get_order_number(page: object, number: int) -> str:
        """Return text of new order number."""
        locator = f"({Account.ORDER_ITEMS_NUMBER})[{number}]"
        return page.locator(locator).inner_text()[2:]

    @staticmethod
    def get_order_price(page: object, number: int) -> str:
        """Return text of new order price."""
        locator = f"({Account.ORDER_ITEMS_PRICE})[{number}]"
        return page.locator(locator).inner_text()

    @staticmethod
    def get_order_icons_locator(number: int) -> str:
        """Return icons locator in order item."""
        locator = f"(({Account.ORDER_ICONS_BOX})" \
                  f"[{number}]{Account.ORDER_ICONS})"
        return locator

    @staticmethod
    def check_bun_ingredients(bun: bool, number: int) -> [bool, int]:
        """Setup bun and ingredients to check icons in order history."""
        if not bun:
            bun = True
            number = 7
        if 5 > number > 1:
            number = 4

        return bun, number
