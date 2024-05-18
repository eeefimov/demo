"""
Description of the functions using at LOGIN Class:
    Fill in email and password fields at Login page.
    Registered user SignIn.
"""
import time
import allure
from pages.base_class import BASEClASS


class LOGIN(BASEClASS):
    """Class with functions for Login page features."""
    LOGIN_LINK = "https://stellarburgers.nomoreparties.site/login"

    TOP_TITLE = "//h2[contains(text(), 'Вход')]"
    EMAIL_FIELD = "input[name=\"name\"]"
    PWD_FIELD = 'input[name=\"Пароль\"]'
    ENTRY_BTN = "//button[contains(text(), 'Войти')]"
    PWD_ERROR = "//p[contains(text(), 'Некорректный пароль')]"
    REGISTRATION_LINK = "//a[contains(text(), 'Зарегистрироваться')]"
    RESTORE_PDW_LINK = "//a[contains(text(), 'Восстановить пароль')]"

    @staticmethod
    def set_login_fields(page: object, mail, pwd) -> None:
        """Fill in email and password fields at Login page."""
        time.sleep(1)
        with allure.step("Fill Email field"):
            page.locator(LOGIN.EMAIL_FIELD).fill(mail)

        with allure.step("Fill PASSWORD field"):
            page.locator(LOGIN.PWD_FIELD).fill(pwd)

        with allure.step("Click Entry button"):
            page.locator(LOGIN.ENTRY_BTN).click()
        time.sleep(2)

    @staticmethod
    @allure.step("User SignIn")
    def user_sign_in(page: object) -> None:
        """Registered user SignIn."""
        with allure.step("Click Account button on Header"):
            page.locator(LOGIN.ACCOUNT_BTN).click()

        LOGIN.set_login_fields(page, LOGIN.mail, LOGIN.pwd)
        time.sleep(2)
