"""
[tests FEATURES]:
    Verify JSON ingredients api data_models = UI data_models.
    Verify ingredient titles with view different values (single eng string).
    Verify ingredient titles with view different values (150 chars string).
    Verify normal view with twice more ingredients on the page.
"""
import logging
import allure
import pytest
import requests
from faker import Faker
from tests.utils import UTILS
from pages.main_page_class import MAIN
from data_models.ingredients_models import IngredientsModel, get_data

fake = Faker()


def test_ingredients_json(page, ingredients):
    """Verify JSON ingredients api data_models = UI data_models."""
    target_url = UTILS.setup_routs(page, ingredients.endpoint, MAIN.link)
    with allure.step('Verify correct url in frontend requests'):
        assert target_url[0]

    with allure.step("Get json from frontend"):
        ui_json = UTILS.get_json_web(page, ingredients.endpoint)
        ui_model = ingredients.get_model(IngredientsModel, get_data(ui_json))

    with allure.step("Get json from backend"):
        try:
            request = ingredients.get_request(ingredients.endpoint)
        except requests.exceptions.HTTPError as errh:
            logging.error(errh)

        if request.status_code == 200:
            api_json = get_data(ingredients.get_request(
                ingredients.endpoint).json())
            api_model = ingredients.get_model(IngredientsModel, api_json)

    with allure.step("Verify frontend json data = backend json data"):
        assert ui_model == api_model


new_values = [
    pytest.param(fake.user_name(), id="single eng string"),
    pytest.param(fake.text(max_nb_chars=50)[:150], id='150 chars string')
]


@pytest.mark.parametrize("new_value", new_values)
def test_ingredients_different_titles(page, ingredients, new_value):
    """Verify ingredient titles with view different values."""
    response = ingredients.get_request(ingredients.endpoint).json()
    modified_response = UTILS.modify_ingredients(response, new_value)
    UTILS.setup_routs(page, ingredients.endpoint, MAIN.link)

    with allure.step('Change ingredients titles'):
        page.route(ingredients.endpoint, lambda route, request: route.fulfill(
            json=modified_response))

    with allure.step('Go to page again'):
        page.goto(MAIN.link)
        page.wait_for_load_state("networkidle")

    with allure.step('Verify visibility of new titles values'):
        for cntr in range(page.locator(MAIN.INGREDIENTS_ITEMS).count()):
            cntr += 1
            title_ui = MAIN.get_ingredients_title(page, cntr)
            title_api = modified_response['data'][cntr - 1]["name"]
            assert str(title_ui.strip()) == str(title_api.strip())


def test_ingredients_double_data(page, ingredients):
    """Verify normal view with twice more ingredients on the page."""
    counter_start = page.locator(MAIN.INGREDIENTS_ITEMS).count()
    response = ingredients.get_request(ingredients.endpoint).json()
    modified_response = UTILS.double_data(response)
    UTILS.setup_routs(page, ingredients.endpoint, MAIN.link)

    with allure.step('Change ingredients item numbers'):
        page.route(ingredients.endpoint, lambda route, request: route.fulfill(
            json=modified_response))

    with allure.step('Go to page again'):
        page.goto(MAIN.link)
        page.wait_for_load_state("networkidle")

    with allure.step('Verify presence of all ingredients'):
        counter_new = page.locator(MAIN.INGREDIENTS_ITEMS).count()
        assert counter_new == counter_start * 2
