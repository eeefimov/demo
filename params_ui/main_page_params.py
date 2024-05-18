"""Params for Main Page."""
from random import randint
import pytest
from pages.main_page_class import MAIN
from pages.login_page_class import LOGIN
from pages.orders_page_class import ORDERS

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
    pytest.param(MAIN.LIST_OF_ORDERS_BTN,
                 ORDERS.TOP_TITLE,
                 id='Redirection to List of orders page'
                 ),
    pytest.param(MAIN.ACCOUNT_BTN,
                 LOGIN.TOP_TITLE,
                 id='Redirection to Account page'
                 )
]
