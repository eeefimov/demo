"""
This module contains tests for Orders page.

[tests DEFINITIONS]:
    Registered user credentials,
    Main page, Orders page,
    Orders Modal window,
    Login page
[TESTS]:
    Verify access to Orders page.
    Verify direct access to Orders page.
    Verify order items have Info window.
    Verify new order added to in progress.
    Verify transfer new order to ready.
    Verify presence of the order total price in order item.
    Verify changes in Total orders number and
    today orders number.
"""
import time
from random import randint
import allure
from playwright.sync_api import expect

from pages.orders_page_class import Orders
from pages.login_page_class import Login
from pages.main_page_class import Main


def test_orders_access(orders_page):
    """Verify access to Orders page."""
    with allure.step('Verify redirection to Orders page'):
        expect(orders_page.locator(Orders.TOP_TITLE)).to_be_visible()


def test_orders_direct_access(page_browser):
    """Verify direct access to Orders page."""
    with allure.step("Set address to the browser"):
        page_browser.goto(Orders.ORDERS_LINK)

    with allure.step('Verify redirection to Orders page'):
        expect(page_browser.locator(Orders.TOP_TITLE)).to_be_visible()


def test_orders_info_window(orders_page):
    """Verify order items have Info window."""
    time.sleep(2)
    counter = orders_page.locator(Orders.ORDER_ITEMS).count()
    item = Orders.get_locator(Orders.ORDER_ITEMS, randint(1, counter))

    with allure.step("Click random order item"):
        orders_page.locator(item).click()

    with allure.step("Verify presence Modal window"):
        expect(orders_page.locator(
            Orders.ORDERS_MODAL_WNDW)).to_be_visible()


def test_orders_in_progress(page):
    """Verify new order added to in progress."""
    Main.make_order(page)
    number = Main.get_order_number(page)
    Main.close_modal_and_redirects(page, Main.LIST_OF_ORDERS_BTN)
    progress = page.locator(Orders.NUMBER_IN_PROGRESS).inner_text()

    with allure.step("Verify new order in progress"):
        assert number == progress[1:]


def test_orders_ready(page):
    """Verify transfer new order to ready."""
    Main.make_order(page)
    number = Main.get_order_number(page)
    Main.close_modal_and_redirects(page, Main.LIST_OF_ORDERS_BTN)
    ready_str = "Все текущие заказы готовы!"

    while page.locator(
            Orders.NUMBER_IN_PROGRESS).inner_text() != ready_str:
        page.reload()

    time.sleep(2)
    ready = page.locator(
        Orders.get_locator(Orders.ORDER_ITEMS_READY, 1)).inner_text()

    with allure.step("Verify orders item in Ready list"):
        assert number == ready[1:]


def test_orders_price(page):
    """Verify presence of the order total price
    in order item."""
    Login.user_sign_in(page)
    Main.add_ingredients(page, True, randint(1, 5))
    order_price = page.locator(Main.TOTAL_PRICE).inner_text()

    with allure.step("Click Order button"):
        page.locator(Main.BOTTOM_BTN).click()

    Main.close_modal_and_redirects(page, Main.LIST_OF_ORDERS_BTN)
    price = Orders.get_locator(Orders.ORDER_PRICE, 1)

    with allure.step("Verify correct new order price"):
        assert order_price == page.locator(price).inner_text()


def test_orders_complete_items(orders_page):
    """Verify changes Total orders number and
    today orders number."""
    all_time_number = int(orders_page.locator(
        Orders.ORDERS_ALLTIME).inner_text())
    today_number = int(orders_page.locator(
        Orders.ORDERS_TODAY).inner_text())

    Main.make_order(orders_page)
    number = int(Main.get_order_number(orders_page))
    Main.close_modal_and_redirects(orders_page, Main.LIST_OF_ORDERS_BTN)

    with allure.step("Verify Total and today number changes"):
        assert number == all_time_number + 1
        assert today_number + 1 == int(orders_page.locator(
            Orders.ORDERS_TODAY).inner_text())
