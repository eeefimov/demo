"""
Description of the functions using at the Reset Class:
    Fill password and Confirm code fields in Reset page.
    Verify confirmation code structure.
"""
import re
import time
import allure
from pages.forgot_page_class import Forgot
PTR = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'


class Reset(Forgot):
    """Class with functions for Reset password page."""
    RESET_LINK = "https://stellarburgers.nomoreparties.site/reset-password"

    PWD_FIELD = 'input[name=\"Введите новый пароль\"]'
    CONFIRM_FIELD = 'input[name=\"name\"]'
    SAVE_BTN = "(//button)[1]"
    PWD_ERROR_MSG = "//p[contains(text(), 'Некорректный пароль')]"

    @staticmethod
    def set_restore_fields(page, pwd, conf_code):
        """Fill password and Confirm code fields in Reset page."""
        with allure.step("Fill Password field"):
            page.locator(Reset.PWD_FIELD).fill(pwd)

        with allure.step("Fill Confirm code field"):
            page.locator(Reset.CONFIRM_FIELD).fill(conf_code)

        with allure.step("Click Save button"):
            page.locator(Reset.SAVE_BTN).click()
        time.sleep(2)

    @staticmethod
    def verify_confirmation_code(code: str) -> bool:
        """Verify confirmation code structure."""
        pattern = PTR
        return bool(re.match(pattern, code))
