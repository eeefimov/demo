# pylint: disable=too-few-public-methods
"""Description BASEClASS Class functions:
    Get locator order item element.
"""
from tests.settings import user_email, user_pass, user_login


class BASEClASS:
    """Base class for UI test."""
    BASE_LINK = "https://stellarburgers.nomoreparties.site/"
    HEADER_SECTION = "//header"
    LOGO = "//div[contains(@class, 'logo')]"
    CONSTRUCTOR_BTN = "//p[contains(text(), 'Конструктор')]"
    LIST_OF_ORDERS_BTN = "//p[contains(text(), 'Лента Заказов')]"
    ACCOUNT_BTN = "//p[contains(text(), 'Личный Кабинет')]"

    mail = user_email
    pwd = user_pass
    name = user_login

    @staticmethod
    def get_locator(locator: str, number: int) -> str:
        """Get locator order item element."""
        return f"({locator})[{number}]"
