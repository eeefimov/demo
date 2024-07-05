"""
This module contains tests for Main page.

[tests DEFINITIONS]:
    Registered user credentials
    Main page
    Login page
    Order Modal window
[TESTS]:
    Verify access to Main page.
    Verify presence of all ingredients items on Main page.
    Verify top titles color changes when scrolling.
    Verify user can drag any single ingredient to Constructor.
    Verify user can drag all ingredients to Constructor.
    Verify ingredients counter changes
    after dragging 3 ingredients to Constructor.
    Verify ingredients counter changes
    after dragging 10 ingredients to Constructor.
    Verify bun's counter changes after dragging to Constructor.
    Verify changing buns in Construction.
    Verify user can delete ingredient from Construction.
    Verify total price changes according to the ingredients
    in the order.
    Verify notification when placing empty order.
    Verify order number with different numbers of ingredient
    (Single bun).
    Verify order number with different numbers of ingredient
    (Bun + single ingredient).
    Verify order number with different numbers of ingredient
    (Not single ingredient).
    Verify order number with different numbers of ingredient
    (No bun, random ingredient number).
    Verify all ingredients title opens window with Nutrition.
    Verify redirection to pages using Header buttons (List of orders).
    Verify redirection to pages using Header buttons (Account page).
"""
import random
import time
import pytest
import allure
from playwright.sync_api import expect

from pages.main_page_class import Main
from pages.login_page_class import Login

from params_ui.main_page_params import counter_changes, \
    different_orders, header_redirection


def test_main_access(page):
    """Verify access to Main page."""
    with allure.step("Verify Main page is opened in the browser"):
        expect(page).to_have_url(Main.link)


def test_main_ingredients_items(page):
    """Verify presence of all ingredients items on Main page."""
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()

    with allure.step("Verify ingredients number"):
        assert counter == Main.ingredients_number


def test_main_top_title_color_changes(page):
    """Verify changes of top titles color when scrolling."""
    page.wait_for_load_state("networkidle")
    with allure.step("Verify elements have proper color"):
        expect(page.locator(Main.TOP_BUN)).to_have_css(
            'color', 'rgb(255, 255, 255)')
        expect(page.locator(Main.TOP_SAUCES)).to_have_css(
            'color', 'rgb(133, 133, 173)')

    with allure.step("Scroll ingredients section to Topping"):
        Main.scroll(page, Main.INSIDE_TOPPING)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

    with allure.step("Verify top titles color is changing"):
        expect(page.locator(Main.TOP_BUN)).to_have_css(
            'color', 'rgb(133, 133, 173)')
        expect(page.locator(Main.TOP_SAUCES)).to_have_css(
            'color', 'rgb(255, 255, 255)')


def test_main_drag_single_ingredient(page):
    """Verify user can drag any single ingredient to Constructor."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()
    for cntr in range(1, counter + 1):
        title = Main.get_ingredients_title(page, cntr)

        with allure.step("Drag ingredient to Constructor"):
            Main.drag_item(page, title, 'empty')

        if cntr in [1, 2]:

            top, bottom = Main.bun_txt(title)

            with allure.step("Verify buns ingredients set in Constructor"):
                expect(page.get_by_text(top)).to_be_visible()
                expect(page.get_by_text(bottom)).to_be_visible()
        else:
            with allure.step("Verify ingredient set in Constructor"):
                title = Main.get_ingredients_title(page, cntr)
                locator = Main.ingredient_in_constructor(title)

                expect(page.locator(locator)).to_be_visible()

        page.reload()


def test_main_drag_all_ingredients(page):
    """Verify user can drag all ingredients to Constructor."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()
    for bun in range(1, 3):
        # Two runs with all ingredients using
        # buns(first, second)
        title = Main.get_ingredients_title(page, bun)
        Main.drag_item(page, title, 'empty')
        top, bottom = Main.bun_txt(title)

        for cntr in range(3, counter):
            title = Main.get_ingredients_title(page, cntr)
            Main.drag_item(page, title, top)
            locator = Main.ingredient_in_constructor(title)

            with allure.step("Verify all ingredients set in Constructor"):
                expect(page.get_by_text(top)).to_be_visible()
                expect(page.get_by_text(bottom)).to_be_visible()
                expect(page.locator(locator)).to_be_visible()

        page.reload()


@pytest.mark.parametrize('number', counter_changes)
def test_main_ingredients_counter_change(page, number):
    """Verify ingredients counter changes
    after dragging to Constructor."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()
    cntr = random.randint(3, counter)   # Using random ingredient (excluding buns)
    title = Main.get_ingredients_title(page, cntr)

    with allure.step("Get start ingredient counter"):
        locator = Main.get_locator(Main.INGREDIENT_COUNTER, cntr)
        start = page.locator(locator).inner_text()

    for _ in range(number):
        Main.drag_item(page, title, 'empty')

    with allure.step("Get finish ingredient counter"):
        finish = page.locator(locator).inner_text()

    with allure.step("verify ingredient counter changed"):
        assert int(start) == 0
        assert int(finish) == number


def test_main_buns_counter_change(page):
    """Verify bun's counter changes
    after dragging to Constructor."""
    for cntr in range(1, 3):
        title = Main.get_ingredients_title(page, cntr)

        with allure.step("Get start bun counter"):
            locator = Main.get_locator(Main.INGREDIENT_COUNTER, cntr)
            start = page.locator(locator).inner_text()
            Main.drag_item(page, title, 'empty')

        with allure.step("Get finish ingredient counter"):
            finish = page.locator(locator).inner_text()

        with allure.step("verify bun counter changed"):
            assert int(start) == 0
            assert int(finish) == 2

        page.reload()

#   ############# Construction section ################


def test_main_buns_changing_in_constructor(page):
    """Verify changing buns in Construction."""
    first_bun_title = Main.get_ingredients_title(page, 1)
    second_bun_title = Main.get_ingredients_title(page, 2)

    Main.drag_item(page, first_bun_title, 'empty')
    bun_top, bun_bottom = Main.bun_txt(first_bun_title)

    with allure.step("Verify first ban set in Constructor"):
        expect(page.get_by_text(bun_top)).to_be_visible()
        expect(page.get_by_text(bun_bottom)).to_be_visible()

    Main.drag_item(page, second_bun_title, bun_top)
    new_top, new_bottom = Main.bun_txt(second_bun_title)

    with allure.step("Verify second bun set in Constructor"):
        expect(page.get_by_text(new_top)).to_be_visible()
        expect(page.get_by_text(new_bottom)).to_be_visible()


def test_main_delete_ingredients(page):
    """Verify user can delete ingredient from Construction."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()
    for cntr in range(3, counter):
        title = Main.get_ingredients_title(page, cntr)
        with allure.step("Drag ingredient to Constructor"):
            Main.drag_item(page, title, 'empty')

            title = Main.get_ingredients_title(page, cntr)
            locator = Main.ingredient_in_constructor(title)

        with allure.step("Verify ingredient set in Constructor"):
            expect(page.locator(locator)).to_be_visible()

        with allure.step("Click Basket Icon"):
            page.locator(Main.BASKET_ICON).click()

        with allure.step("Verify ingredient deleted from Constructor"):
            expect(page.locator(locator)).not_to_be_visible()

        page.reload()


def test_main_total_price_changing(page):
    """Verify total price changes according
    to the ingredients in the order."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()

    for cntr in range(1, counter):
        title = Main.get_ingredients_title(page, cntr)
        price_locator = Main.get_locator(Main.INGREDIENT_PRICE, cntr)
        ingr_price = page.locator(price_locator).inner_text()

        with allure.step("Drag ingredient to Constructor"):
            Main.drag_item(page, title, 'empty')

        total_price = page.locator(Main.TOTAL_PRICE).inner_text()

        with allure.step("Verify total price changed"
                         "according to ingredient price"):
            if cntr in [1, 2]:
                assert int(total_price) == int(ingr_price) * 2
            else:
                assert int(total_price) == int(ingr_price)

        page.reload()


@allure.issue("Modal window Label txt is "
              "'Your order is being prepared.' "
              "with empty order")
def test_main_order_empty(page):
    """Verify notification when placing empty order."""
    Login.user_sign_in(page)

    with allure.step("Click Order button"):
        page.locator(Main.BOTTOM_BTN).click()
        time.sleep(1)

    with allure.step("Verify empty Order notification text"):
        txt = page.locator(Main.IN_PROGRESS_TITLE).inner_text()
        assert txt != "Ваш заказ начали готовить"


@pytest.mark.parametrize("bun, number", different_orders)
def test_main_order_not_empty(page, bun, number):
    """Verify order number with different numbers of ingredient."""
    Main.make_order(page, bun=bun, number=number)

    if bun:
        with allure.step("Verify order number is not 9999"):
            assert int(Main.get_order_number(page)) != 9999
    else:
        with allure.step("Verify order number is 9999"):
            # User can't place an order without buns
            assert int(Main.get_order_number(page)) == 9999


def test_main_nutrition_wnd(page):
    """Verify all ingredients title opens window with Nutrition."""
    counter = page.locator(Main.INGREDIENTS_ITEMS).count()

    for cntr in range(1, counter):
        title = Main.get_ingredients_title(page, cntr)

        with allure.step("Click ingredient title"):
            page.get_by_text(title).click()

        with allure.step("Verify presence of Nutrition window"):
            expect(page.locator(Main.NUTRITION_X_BTN)).to_be_visible()

        with allure.step("Click 'x' in Nutrition window"):
            page.locator(Main.NUTRITION_X_BTN).click()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_main_header_btns(page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click on button at Header"):
        page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(page.locator(exp)).to_be_visible()
