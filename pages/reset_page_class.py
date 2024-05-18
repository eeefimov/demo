"""
Description of the functions using at the RESET Class:
    Fill password and Confirm code fields in Reset page.
    Verify confirmation code structure.
"""
import re
import time
import allure
from pages.forgot_page_class import FORGOT
PTR = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'


class RESET(FORGOT):
    """Class with functions for RESET password page."""
    RESET_LINK = "https://stellarburgers.nomoreparties.site/reset-password"

    PWD_FIELD = 'input[name=\"Введите новый пароль\"]'
    CONFIRM_FIELD = 'input[name=\"name\"]'
    SAVE_BTN = "(//button)[1]"
    PWD_ERROR_MSG = "//p[contains(text(), 'Некорректный пароль')]"

    @staticmethod
    def set_restore_fields(page, pwd, conf_code):
        """Fill password and Confirm code fields in Reset page."""
        with allure.step("Fill Password field"):
            page.locator(RESET.PWD_FIELD).fill(pwd)

        with allure.step("Fill Confirm code field"):
            page.locator(RESET.CONFIRM_FIELD).fill(conf_code)

        with allure.step("Click Save button"):
            page.locator(RESET.SAVE_BTN).click()
        time.sleep(2)

    @staticmethod
    def verify_confirmation_code(code: str) -> bool:
        """Verify confirmation code structure."""
        pattern = PTR
        return bool(re.match(pattern, code))
