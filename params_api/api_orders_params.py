"""Params for orders api"""
from random import randint
import pytest
from faker import Faker

fake = Faker()

# orders with different numbers of ingredients
order_length = [
    pytest.param(True, 1, id='Order with bun and 1 ingredient'),
    pytest.param(False, 3, id='Order with no bun and 3 ingredient')
]

# different orders configuration
order_config = [
    pytest.param(True, False, 1, 0, 400,
                 id='Empty order'),
    pytest.param(False, True, 1, randint(1, 10), 200,
                 id='Order with 1 bun and ingredients [1 to 10]'),
    pytest.param(False, True, 1, 100, 200,
                 id='Order with 1 bun and 100 ingredients'),
    pytest.param(False, False, 1, randint(1, 10), 200,
                 id='Order with no bun and ingredients [1 to 10]'),
    pytest.param(False, True, randint(1, 5), randint(1, 5), 200,
                 id='Order buns [1 to 5] and ingredients [1 to 5]'),
]

# different numbers of orders for one session
number_of_orders = [
    pytest.param(1, id='Single order'),
    pytest.param(3, id='3 orders'),
    pytest.param(20, id='20 order')
]

# invalid token for orders
invalid_token = [
    pytest.param('', 401,
                 id='Empty token'),
    pytest.param(fake.sha1(raw_output=False), 401,
                 id='Invalid token'),
]
