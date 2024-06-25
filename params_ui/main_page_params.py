"""Params for Main Page."""
from random import randint
import pytest
from pages.main_page_class import Main
from pages.login_page_class import Login
from pages.orders_page_class import Orders

# Counter limits for ingredients.
counter_changes = [
    pytest.param(3, id="Verify 3 ingredients counter"),
    pytest.param(10, id="Verify 10 ingredients counter"),
]

# Order with different configurations.
different_orders = [
    pytest.param(True, 0,
                 id="Single bun"),
    pytest.param(True, 1,
                 id="Bun + single ingredient"),
    pytest.param(True, randint(2, 4),
                 id="Bun + not single ingredient"),
    pytest.param(False, randint(1, 10),
                 id="No bun, random ingredient number")
]

# Validation Header buttons.
header_redirection = [
    pytest.param(Main.LIST_OF_ORDERS_BTN,
                 Orders.TOP_TITLE,
                 id='Redirection to List of orders page'
                 ),
    pytest.param(Main.ACCOUNT_BTN,
                 Login.TOP_TITLE,
                 id='Redirection to Account page'
                 )
]
