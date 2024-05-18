# pylint: disable=too-few-public-methods
"""Class holds all endpoints for tests."""
MAIN_URL = "https://stellarburgers.nomoreparties.site/api/"


class ENDPOINTS:
    """Class holds all endpoints for tests."""
    ingredients = f"{MAIN_URL}ingredients"
    orders = f"{MAIN_URL}orders"
    orders_all = f"{MAIN_URL}orders/all"
    reset_pwd = f"{MAIN_URL}password-reset"
    register = f"{MAIN_URL}auth/register"
    login = f"{MAIN_URL}auth/login"
    logout = f"{MAIN_URL}auth/logout"
    token = f"{MAIN_URL}auth/token"
    user = f"{MAIN_URL}auth/user"
    delete = f"{MAIN_URL}auth/delete"
