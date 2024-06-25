"""
Description of the functions using at the Orders Class:
    Get last order number from Orders page.
"""
import allure
from pages.base_class import BaseClass


class Orders(BaseClass):
    """
    Class with functions for Orders page feature.
    """
    ORDERS_LINK = "https://stellarburgers.nomoreparties.site/feed"

    TOP_TITLE = "//h1[contains(text(), 'Лента заказов')]"
    ORDER_ITEMS = "//li[contains(@class, 'listItem')]"
    ORDERS_NUMBER = "(//p[contains(@class, 'digits-default')])"
    NUMBER_IN_PROGRESS = "//ul[contains(@class, 'orderListReady')]/li"
    ORDER_ITEMS_READY = "//li[contains(@class, 'mb-2')]"
    ORDERS_MODAL_WNDW = "//div[contains(@class, 'Modal_orderBox')]"
    ORDER_PRICE = "//div/p[@class='text text_type_digits-default mr-2']"
    ORDERS_ALLTIME = "(//p[contains(@class, 'digits-large')])[1]"
    ORDERS_TODAY = "(//p[contains(@class, 'digits-large')])[2]"

    @staticmethod
    @allure.step("Get last order number from Orders page")
    def get_last_order_number(page: object) -> int:
        """Get last order number from Orders page"""
        old_number = page.locator(f"{Orders.ORDERS_NUMBER}[1]").inner_text()
        return int(old_number[2:])
