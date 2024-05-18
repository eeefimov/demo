"""UI and API tests configuration."""
# pylint: disable=redefined-outer-name
# pylint: disable=attribute-defined-outside-init)
import pytest
import allure
from faker import Faker
from playwright.sync_api import sync_playwright
from api.user import USER
from api.orders import ORDERS
from api.ingredients import INGREDIENTS
from tests.utils import UTILS
from pages.base_class import BASEClASS
from pages.login_page_class import LOGIN
fake = Faker()


@pytest.fixture(scope="function")
def page_browser():
    """Fixture to set up the browser page for testing."""
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        viewport_size = {"width": 1280, "height": 1024}
        page.set_viewport_size(viewport_size)

        with allure.step("Go to site"):
            page.goto(BASEClASS.BASE_LINK)

        yield page

        UTILS.add_screenshot(page)
        browser.close()


@pytest.fixture(scope="function")
def page(page_browser):
    """Base page fixture"""
    return page_browser


@pytest.fixture(scope="function")
def register_page(page_browser):
    """Registration page fixture"""
    with allure.step("Click Account button on Header"):
        page_browser.locator(BASEClASS.ACCOUNT_BTN).click()

    with allure.step("Click Registration link"):
        page_browser.locator(LOGIN.REGISTRATION_LINK).click()

    return page_browser


@pytest.fixture(scope="function")
def login_page(page_browser):
    """Login page fixture"""
    with allure.step("Click Account button on Header"):
        page_browser.locator(BASEClASS.ACCOUNT_BTN).click()

    return page_browser


@pytest.fixture(scope="function")
def account_page(page_browser):
    """Account page fixture"""
    LOGIN.user_sign_in(page_browser)

    with allure.step("Click Account button on Header"):
        page_browser.locator(LOGIN.ACCOUNT_BTN).click()

    return page_browser


@pytest.fixture(scope="function")
def forgot_page(page_browser):
    """Reset password fixture"""
    with allure.step("Click Account button on Header"):
        page_browser.locator(BASEClASS.ACCOUNT_BTN).click()

    with allure.step("Click Restore password link"):
        page_browser.locator(LOGIN.RESTORE_PDW_LINK).click()

    return page_browser


@pytest.fixture(scope="function")
def orders_page(page_browser):
    """Orders page fixture"""
    with allure.step("Click List of Orders button on Header"):
        page_browser.locator(BASEClASS.LIST_OF_ORDERS_BTN).click()
    return page_browser


@pytest.fixture(scope="function")
def ingredients():
    """Fixture to set up api ingredients."""
    with allure.step("Setup Ingredients"):
        ingredients = INGREDIENTS()
    return ingredients


@pytest.fixture(scope="function")
def orders():
    """Fixture to set up api orders."""
    with allure.step("Setup Orders"):
        orders = ORDERS()
    return orders


@pytest.fixture
def register():
    """Fixture to set up api register."""
    with allure.step("Setup Register data"):
        register = USER()
        name = f'{fake.text()[:5]}{fake.user_name()}'
        mail = f"{fake.first_name()}.{fake.last_name()}@"\
               f"{fake.domain_name()}"
        pwd = fake.password()[:6]
        register.data = register.setup_register_data(name, mail, pwd)

    yield register

    register.delete_user(register.access_token)


@pytest.fixture
def logout(register):
    """Fixture to set up api logout."""
    logout = USER()
    with allure.step("Setup logout data"):
        logout.data = register.data
    response = logout.post_register()
    logout.access_token = response.json().get("refreshToken")

    yield logout


@pytest.fixture
def usr(register):
    """Fixture to set up api user."""
    usr = USER()
    with allure.step("Setup User data"):
        usr.data = register.data
    response = usr.post_register()
    usr.access_token = response.json().get("accessToken")
    usr.header = usr.header_auth(usr.access_token)
    yield usr


@pytest.fixture
def user_order():
    """Fixture to set up api user order."""
    with allure.step("Setup Make Order"):
        class USERORDERS(USER, ORDERS):
            """Class for authorized user
            make an orders"""
            def __init__(self):
                USER.__init__(self)
                ORDERS.__init__(self)
        user_order = USERORDERS()
        # prepare user data
        name = f'{fake.text()[:5]}{fake.user_name()}'
        mail = f"{fake.first_name()}.{fake.last_name()}@" \
               f"{fake.domain_name()}"
        pwd = fake.password()[:6]
        user_order.endpoint = user_order.endpoints.register
        user_order.data = user_order.setup_register_data(name, mail, pwd)
        # register new user
        response = user_order.post_register()
        # setup user header with token
        user_order.access_token = response.json().get("accessToken")
        user_order.header = user_order.header_auth(user_order.access_token)
        # prepare ingredients for order
        user_order.ingredients = user_order.load_data_from_file(
            "ingredients.json")
        # setup order endpoint
        user_order.endpoint = user_order.endpoints.orders

        yield user_order

        user_order.delete_user(user_order.access_token)


@pytest.fixture
def reset(register):
    """Fixture to set up api reset user password."""
    register.setup_reset(register)
    return register
