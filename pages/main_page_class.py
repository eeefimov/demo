"""
Description of the functions using at MAIN Class:
    Scroll Ingredient section.
    Get text of ingredient title.
    Return locator of ingredient dragged to Constructor.
    Drag ingredient to Constructor.
    Drag bun to Construction.
    Drag ingredient to bun in Construction.
    Get two locators of bun dragged to Constructor.
    Get order number.
    Add random ingredients to order.
    Sign in, add ingredients and make an order.
    Close order modal window and redirects to page.
"""
import time
from random import randint
import allure
from pages.base_class import BASEClASS
from pages.login_page_class import LOGIN


class MAIN(BASEClASS):
    """Class with functions for Main page features."""
    link = "https://stellarburgers.nomoreparties.site/"
    BOTTOM_BTN = "(//div/button)[1]"

    TOP_TITLE = "//h1[contains(text(),'Соберите бургер')]"
    TOP_BUN = "//span[contains(text(), 'Булки')]"
    TOP_SAUCES = "//span[contains(text(), 'Соусы')]"
    INSIDE_TOPPING = "//h2[contains(text(), 'Начинки')]"
    INGREDIENT_COUNTER = "//p[contains(@class, 'counter_counter')]"
    INGREDIENT_PRICE = "//p[contains(@class, '__price__')]"

    TOTAL_PRICE = "//p[@class='text text_type_digits-medium mr-3']"
    BASKET_ICON = "(//span[@class='constructor-element__action pr-2'])[2]"
    ORDER_WINDOW = "(//div[contains(@class, 'Modal_modal')])[1]"
    IN_PROGRESS_TITLE = "//p[contains(@class, 'text_type_main-small')]"
    ORDER_NUMBER = "//h2[contains(@class, 'text_type_digits')]"

    INGREDIENTS_ITEMS = "//ul/a"
    NUTRITION_TOP_TITLE = "Детали ингредиента"
    NUTRITION_X_BTN = "(//button[contains(@class, 'close')])[1]"

    ingredients_number = 15

    @staticmethod
    @allure.step('Scroll Ingredients')
    def scroll(page: object, element: str) -> None:
        """Scroll Ingredient section."""
        with allure.step(f"Scroll to {element}"):
            page.locator(element).scroll_into_view_if_needed()

    @staticmethod
    def get_ingredients_title(page: object, number: int) -> str:
        """Get text of ingredient title."""
        locator = (
            "//ul[contains(@class, 'ingredients__list')]"
            "//p[contains(@class, 'ingredient__text')]"
        )
        return page.locator(f"({locator})[{number}]").inner_text()

    @staticmethod
    def ingredient_in_constructor(title: str) -> str:
        """Return locator of ingredient dragged to Constructor."""
        locator = \
            f"//span[@class='constructor-element__text' and text()='{title}']"
        return locator

    @staticmethod
    @allure.step("Drag ingredients to Constructor")
    def drag_item(page: object, title: str, condition: str) -> None:
        """Drag ingredient to Constructor."""
        if title in {"Флюоресцентная булка R2-D3", "Краторная булка N-200i"}:
            text = 'bun'
        else:
            text = 'ingredient'

        with allure.step(f"Drag {text} to Constructor"):
            if condition == 'empty':
                cnstrctr = "Перетяните булочку сюда (верх)0"
                page.locator(f"//p[contains(text(), '{title}')]").drag_to(
                    page.get_by_text(f"{cnstrctr}"))
            else:
                cnstrctr = condition
                page.locator(f"//p[contains(text(), '{title}')]").drag_to(
                    page.get_by_text(f"{cnstrctr}"))
        time.sleep(2)

    @staticmethod
    @allure.step("Drag bun to Construction")
    def drag_bun(page: object, bun_number: int) -> None:
        """Drag bun to Construction."""
        title = MAIN.get_ingredients_title(page, bun_number)
        MAIN.drag_item(page, title, 'empty')

    @staticmethod
    def drag_ingredient_to_bun(page: object, title: str) -> None:
        """Drag ingredient to bun in Construction."""
        top, _ = MAIN.bun_txt(title)
        cntr = randint(3, 15)
        title = MAIN.get_ingredients_title(page, cntr)
        MAIN.drag_item(page, title, top)

    @staticmethod
    def bun_txt(title) -> [str, str]:
        """Get two locators of bun dragged to Constructor."""
        bun_txt_top = f"{title} (верх)"
        bun_txt_bottom = f"{title} (низ)"
        return bun_txt_top, bun_txt_bottom

    @staticmethod
    def get_order_number(page: object) -> str:
        """Get order number."""
        locator = f"{MAIN.ORDER_NUMBER}"
        return page.locator(locator).inner_text()

    @staticmethod
    @allure.step("Make an order with random ingredients")
    def add_ingredients(page: object, bun: bool, ingredients_num: int) -> None:
        """Add random ingredients to order."""
        # single bun
        if bun and ingredients_num == 0:
            MAIN.drag_bun(page, randint(1, 2))

        # single bun + 1 ingredient
        elif bun and ingredients_num == 1:
            bun = randint(1, 2)
            MAIN.drag_bun(page, bun)
            bun_title = MAIN.get_ingredients_title(page, bun)
            MAIN.drag_ingredient_to_bun(page, bun_title)

        # single bun + not single ingredient
        elif bun and ingredients_num > 1:
            bun = randint(1, 2)
            MAIN.drag_bun(page, bun)
            bun_title = MAIN.get_ingredients_title(page, bun)

            for _ in range(ingredients_num):
                MAIN.drag_ingredient_to_bun(page, bun_title)

        # no bun
        if not bun and ingredients_num > 0:
            for _ in range(ingredients_num):
                ingr = randint(3, 15)
                title = MAIN.get_ingredients_title(page, ingr)
                MAIN.drag_item(page, title, 'empty')

    @staticmethod
    @allure.step("Make an Order")
    def make_order(page: object, bun=True, number=randint(1, 5)) -> None:
        """Sign in, add ingredients and make an order."""
        LOGIN.user_sign_in(page)
        MAIN.add_ingredients(page, bun, number)

        with allure.step("Click Order button"):
            page.locator(MAIN.BOTTOM_BTN).click()
            time.sleep(3)

    @staticmethod
    def close_modal_and_redirects(page: object, locator) -> None:
        """Close order modal window and redirects to page."""
        text = None
        with allure.step("Click 'x' in Nutrition window"):
            page.locator(MAIN.NUTRITION_X_BTN).click()

        if locator == MAIN.ACCOUNT_BTN:
            text = "Account"
        if locator == MAIN.LIST_OF_ORDERS_BTN:
            text = "List of Orders"

        with allure.step(f"Click {text} button"):
            page.locator(locator).click()
        time.sleep(2)
