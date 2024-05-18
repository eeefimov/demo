"""
Description FORGOT Class functions:
    Fill email field in Forgot page.
"""
import time
import allure
from pages.base_class import BASEClASS
from tests.settings import gmail_password_registered, gmail_user_registered


class FORGOT(BASEClASS):
    """Class with functions for FORGOT password page."""
    FORGOT_LINK = "https://stellarburgers.nomoreparties.site/forgot-password"

    TOP_TITLE = "//h2[contains(text(), 'Восстановление пароля')]"
    EMAIL_FIELD = "input[name=\'name\']"
    RESTORE_BTN = "(//button)[1]"
    ENTRY_LINK = "//a[contains(text(), 'Войти')]"

    registered_gmail = gmail_user_registered
    registered_pwd = gmail_password_registered

    @staticmethod
    def fill_forgot_field(page, email_value):
        """Fill email field in Forgot page."""
        with allure.step("Fill email field"):
            page.locator(FORGOT.EMAIL_FIELD).fill(email_value)

        with allure.step("Click Restore button"):
            page.locator(FORGOT.RESTORE_BTN).click()
            time.sleep(2)
