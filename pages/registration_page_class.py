"""
Description of the functions using at the USER Class:
    Fill in a post_login, an email, and password fields.
"""
import time
import allure
from pages.base_class import BaseClass


class Register(BaseClass):
    """
    Class with functions for Registration page features.
    """
    REGISTER_LINK = "https://stellarburgers.nomoreparties.site/register"

    TOP_TITLE = "//h2[contains(text(), 'Регистрация')]"
    REGISTRATION_BTN = "//button[contains(text(), 'Зарегистрироваться')]"
    PWD_ERROR = "//p[contains(text(), 'Некорректный пароль')]"
    USER_ERROR = "//p[contains(text(), 'Такой пользователь уже существует')]"
    MAIL_ERROR = "//p[contains(text(), 'Такой пользователь уже существует')]"
    ENTRY_LINK = "//a[contains(text(), 'Войти')]"

    @staticmethod
    def fill_register_fields_and_click(page: object, login, email, password) -> None:
        """Fill in a post_login, an email, and password fields."""
        with allure.step("Fill in Login field"):
            page.locator("fieldset").filter(
                has_text="Имя").get_by_role("textbox").fill(login)

        with allure.step("Fill in Email field"):
            page.locator("fieldset").filter(
                has_text="Email").get_by_role("textbox").fill(email)

        with allure.step("Fill in Password field"):
            page.locator("fieldset").filter(
                has_text="Пароль").get_by_role("textbox").fill(password)

        with allure.step("Click Registration button"):
            page.locator(Register.REGISTRATION_BTN).click()
            time.sleep(1)
