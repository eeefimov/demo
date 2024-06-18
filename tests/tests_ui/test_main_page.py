"""
This module contains tests for Main page.

[tests DEFINITIONS]:
    Registered user credentials
    Main page
    Login page
    Order Modal window
[TESTS]:
    Verify access to Main page.
    Verify all ingredients items presence on Main page.
    Verify top titles color changes when scrolling.
    Verify user can drag a single ingredient to Constructor.
    Verify user can drag all ingredient to Constructor.
    Verify ingredients counter changes after dragging
    3 ingredients to Constructor.
    Verify ingredients counter changes after dragging
    10 ingredients to Constructor.
    Verify bun's counter changes after dragging to Constructor.
    Verify buns change in Construction.
    Verify user can delete an ingredient from Construction.
    Verify total price changes according to the ingredients
    in the order.
    Verify order empty.
    Verify order with Single bun.
    Verify order with Bun + single ingredient.
    Verify order with Bun + not single ingredient.
    Verify order with No bun, random ingredient number.
    Verify all ingredient title open window with Nutrition.
    Verify redirection to pages using Header buttons (List of orders).
    Verify redirection to pages using Header buttons (Account page).
"""
import time
import pytest
import allure
from playwright.sync_api import expect

from pages.main_page_class import MAIN
from pages.login_page_class import LOGIN

from params_ui.main_page_params import counter_changes, \
    different_orders, header_redirection


def test_main_access(page):
    """Verify access to Main page."""
    with allure.step("Check access to Main page"):
        expect(page).to_have_url(MAIN.link)


def test_main_ingredients_items(page):
    """Verify all ingredients items presence on Main page."""
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()

    with allure.step("Verify numbers of elements"):
        assert counter == MAIN.ingredients_number


def test_main_top_title_color_changes(page):
    """Verify top titles color changes when scrolling."""
    with allure.step("Verify elements have proper color"):
        expect(page.locator(MAIN.TOP_BUN)).to_have_css(
            'color', 'rgb(255, 255, 255)')
        expect(page.locator(MAIN.TOP_SAUCES)).to_have_css(
            'color', 'rgb(133, 133, 173)')

    with allure.step("Scroll ingredients section to Topping"):
        MAIN.scroll(page, MAIN.INSIDE_TOPPING)
        time.sleep(2)

    with allure.step("Verify top titles color changing"):
        expect(page.locator(MAIN.TOP_BUN)).to_have_css(
            'color', 'rgb(133, 133, 173)')
        expect(page.locator(MAIN.TOP_SAUCES)).to_have_css(
            'color', 'rgb(255, 255, 255)')


def test_main_drag_single_ingredient(page):
    """Verify user can drag a single ingredient to Constructor."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()
    for cntr in range(counter):
        cntr += 1

        title = MAIN.get_ingredients_title(page, cntr)

        with allure.step("Drag ingredient to Constructor"):
            MAIN.drag_item(page, title, 'empty')

        if cntr in [1, 2]:

            top, bottom = MAIN.bun_txt(title)

            with allure.step("Verify buns ingredients set in Constructor"):
                expect(page.get_by_text(top)).to_be_visible()
                expect(page.get_by_text(bottom)).to_be_visible()
        else:
            with allure.step("Verify ingredient set in Constructor"):
                title = MAIN.get_ingredients_title(page, cntr)
                locator = MAIN.ingredient_in_constructor(title)

                expect(page.locator(locator)).to_be_visible()

        page.reload()


def test_main_drag_all_ingredients(page):
    """Verify user can drag all ingredient to Constructor."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()
    for bun in range(1, 3):
        title = MAIN.get_ingredients_title(page, bun)
        MAIN.drag_item(page, title, 'empty')
        top, bottom = MAIN.bun_txt(title)
        for cntr in range(3, counter + 1):
            title = MAIN.get_ingredients_title(page, cntr)
            MAIN.drag_item(page, title, top)
            locator = MAIN.ingredient_in_constructor(title)

            with allure.step("Verify all ingredients set in Constructor"):
                expect(page.get_by_text(top)).to_be_visible()
                expect(page.get_by_text(bottom)).to_be_visible()
                expect(page.locator(locator)).to_be_visible()

        page.reload()


@pytest.mark.parametrize('number', counter_changes)
def test_main_ingredients_counter_change(page, number):
    """Verify ingredients counter changes
    after dragging to Constructor."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()
    for cntr in range(2, counter):
        cntr += 1
        title = MAIN.get_ingredients_title(page, cntr)

        with allure.step("Get start ingredient counter"):
            locator = MAIN.get_locator(MAIN.INGREDIENT_COUNTER, cntr)
            start = page.locator(locator).inner_text()

        for _ in range(number):
            MAIN.drag_item(page, title, 'empty')

        with allure.step("Get finish ingredient counter"):
            finish = page.locator(locator).inner_text()

        with allure.step("verify ingredient counter changed"):
            assert int(start) == 0
            assert int(finish) == number


def test_main_buns_counter_change(page):
    """Verify bun's counter changes
    after dragging to Constructor."""
    for cntr in range(1, 3):
        title = MAIN.get_ingredients_title(page, cntr)

        with allure.step("Get start bun counter"):
            locator = MAIN.get_locator(MAIN.INGREDIENT_COUNTER, cntr)
            start = page.locator(locator).inner_text()
            MAIN.drag_item(page, title, 'empty')

        with allure.step("Get finish ingredient counter"):
            finish = page.locator(locator).inner_text()

        with allure.step("verify bun counter changed"):
            assert int(start) == 0
            assert int(finish) == 2

        page.reload()

#   ############# Construction section ################


def test_main_buns_changing_in_constructor(page):
    """Verify bus change in Construction."""
    first_bun_title = MAIN.get_ingredients_title(page, 1)
    second_bun_title = MAIN.get_ingredients_title(page, 2)

    MAIN.drag_item(page, first_bun_title, 'empty')
    bun_top, bun_bottom = MAIN.bun_txt(first_bun_title)

    with allure.step("Verify first ban set in Constructor"):
        expect(page.get_by_text(bun_top)).to_be_visible()
        expect(page.get_by_text(bun_bottom)).to_be_visible()

    MAIN.drag_item(page, second_bun_title, bun_top)
    new_top, new_bottom = MAIN.bun_txt(second_bun_title)

    with allure.step("Verify second bun set in Constructor"):
        expect(page.get_by_text(new_top)).to_be_visible()
        expect(page.get_by_text(new_bottom)).to_be_visible()


def test_main_delete_ingredients(page):
    """Verify user can delete ingredient from Construction."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()
    for cntr in range(2, counter):
        cntr += 1
        title = MAIN.get_ingredients_title(page, cntr)
        with allure.step("Drag ingredient to Constructor"):
            MAIN.drag_item(page, title, 'empty')

            title = MAIN.get_ingredients_title(page, cntr)
            locator = MAIN.ingredient_in_constructor(title)

        with allure.step("Verify ingredient set in Constructor"):
            expect(page.locator(locator)).to_be_visible()

        with allure.step("Click Basket Icon"):
            page.locator(MAIN.BASKET_ICON).click()

        with allure.step("Verify ingredient deleted from Constructor"):
            expect(page.locator(locator)).not_to_be_visible()

        page.reload()


def test_main_total_price_changing(page):
    """Verify total price changes according
    to the ingredients in the order."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()

    for cntr in range(counter):
        cntr += 1
        title = MAIN.get_ingredients_title(page, cntr)
        price_locator = MAIN.get_locator(MAIN.INGREDIENT_PRICE, cntr)
        ingr_price = page.locator(price_locator).inner_text()

        with allure.step("Drag ingredient to Constructor"):
            MAIN.drag_item(page, title, 'empty')

        total_price = page.locator(MAIN.TOTAL_PRICE).inner_text()

        with allure.step("Verify total price changed"
                         "according to ingredient price"):
            if cntr in [1, 2]:
                assert int(total_price) == int(ingr_price) * 2
            else:
                assert int(total_price) == int(ingr_price)

        page.reload()


def test_main_order_empty(page):
    """Verify order empty."""
    LOGIN.user_sign_in(page)

    with allure.step("Click Order button"):
        page.locator(MAIN.BOTTOM_BTN).click()
        time.sleep(1)

    with allure.step("Verify empty Order not ordered"):
        txt = page.locator(MAIN.IN_PROGRESS_TITLE).inner_text()
        assert txt != "Ваш заказ начали готовить"


@pytest.mark.parametrize("bun, number", different_orders)
def test_main_order_not_empty(page, bun, number):
    """Verify order single ingredient."""
    MAIN.make_order(page, bun=bun, number=number)

    with allure.step("Verify order number is not 9999"):
        assert int(MAIN.get_order_number(page)) != 9999


def test_main_nutrition_wnd(page):
    """Verify all ingredient title open window with Nutrition."""
    counter = page.locator(MAIN.INGREDIENTS_ITEMS).count()

    for cntr in range(counter):
        cntr += 1
        title = MAIN.get_ingredients_title(page, cntr)

        with allure.step("Click ingredient title"):
            page.get_by_text(title).click()

        with allure.step("Verify presence of Nutrition window"):
            expect(page.locator(MAIN.NUTRITION_X_BTN)).to_be_visible()

        with allure.step("Click 'x' in Nutrition window"):
            page.locator(MAIN.NUTRITION_X_BTN).click()


@pytest.mark.parametrize('btn, exp', header_redirection)
def test_main_header_btns(page, btn, exp):
    """Verify redirection to pages using Header buttons."""
    with allure.step("Click on button at Header"):
        page.locator(btn).click()

    with allure.step("Verify redirection to page"):
        expect(page.locator(exp)).to_be_visible()
