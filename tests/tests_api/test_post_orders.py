"""
This module contains tests for POST /orders endpoint.

[tests DEFINITIONS]:
    Post request for /auth/register endpoint.
    Patch request for /auth/user endpoint.
    Get request for /auth/user endpoint.
    Post request for /auth/register endpoint.
    User access_token.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify values type in response.
    Verify number of ingredients in response
        (Order with bun and 1 ingredient).
    Verify number of ingredients in response
        (Order with no bun and 3 ingredient).
    Verify different types of orders (Empty order: 400).
    Verify different types of orders
        (Order with 1 bun and ingredients [1 to 10]: 200).
    Verify different types of orders
        (Order with 1 bun and 100 ingredients: 200).
    Verify different types of orders
        (Order with no bun and ingredients [1 to 10]: 200).
    Verify different types of orders
        (Order buns [1 to 5] and ingredients [1 to 5]: 200).
    Verify new user order in response (Single order).
    Verify new user order in response (3 orders).
    Verify new user order in response (20 order).
    Verify response error message with invalid token
        (Empty token).
    Verify response error message with invalid token
        (Invalid token).
    Verify changes of total and totalToday numbers.
    Verify changes of total and totalToday numbers in all_orders.
    Verify price of order with bun.
    Verify response code with invalid token (Empty token: 401).
    Verify response code with invalid token (Invalid token: 401).
"""
import allure
import pytest
from data_models.orders_model import OrderResponse, OrdersModel
from data_models.user_model import MsgModel

from params_api.api_orders_params import order_length, \
    order_config, number_of_orders, invalid_token


class TestUserOrder:
    """Class for testing Post /orders endpoint."""
    def test_status_code(self, user_order):
        """Verify response status code."""
        response = user_order.do_order(user_order)
        assert response.status_code == 200

    def test_response_payload(self, user_order):
        """Verify exist of payload in response."""
        response = user_order.do_order(user_order)
        assert response.json()

    def test_payload_type_validation(self, user_order):
        """Verify values type in response."""
        response = user_order.do_order(user_order)
        model = user_order.get_model(OrderResponse, response.json())
        assert isinstance(model, OrderResponse)

    @pytest.mark.parametrize('buns, number', order_length)
    def test_items_number_in_order(self, user_order, buns, number):
        """Verify number of ingredients in response."""
        order = user_order.setup_order(buns=buns, ingr_number=number)
        response = user_order.send_requests('post',
                                            user_order.endpoint,
                                            user_order.header,
                                            order)
        if buns:
            assert (len(response.json()['order']['ingredients'])) == number + 1
        else:
            assert (len(response.json()['order']['ingredients'])) == number

    # pylint: disable=too-many-arguments
    @pytest.mark.parametrize('emty, buns, b_number, '
                             'number, exp', order_config)
    def test_order_configur(self, user_order, emty, exp, b_number,
                            buns, number):
        """Verify different types of orders."""
        order = user_order.setup_order(empty=emty, buns=buns,
                                       buns_number=b_number,
                                       ingr_number=number)
        response = user_order.send_requests('post',
                                            user_order.endpoint,
                                            user_order.header,
                                            order)
        assert response.status_code == exp
        if not emty:
            model = user_order.get_model(OrderResponse, response.json())
            assert isinstance(model, OrderResponse)
            if buns:
                assert (len(response.json(
                )['order']['ingredients'])) == number + b_number
            else:
                assert (len(response.json(
                )['order']['ingredients'])) == number

    @pytest.mark.parametrize('number', number_of_orders)
    def test_get_user_orders(self, user_order, number):
        """Verify new user order in response."""
        for _ in range(0, number):
            user_order.do_order(user_order)
        response = user_order.send_requests('get',
                                            user_order.endpoint,
                                            user_order.header, None)
        assert response.status_code == 200
        model = user_order.get_model(OrdersModel, response.json())
        assert isinstance(model, OrdersModel)
        assert len(response.json()['orders']) == number

    @pytest.mark.parametrize('auth, exp', invalid_token)
    def test_get_user_orders_invalid_auth(self, user_order, auth, exp):
        """Verify response error message with invalid token."""
        user_order.header = user_order.header_auth(auth)
        response = user_order.send_requests('get', user_order.endpoint,
                                            user_order.header, None)
        assert response.status_code == exp
        response_model = user_order.get_model(MsgModel,
                                              response.json())
        error_model = user_order.get_model(MsgModel,
                                           user_order.authorisation)
        assert response_model == error_model

    def test_orders_number_changes(self, user_order):
        """Verify changes of total and totalToday numbers."""
        total_start, total_today_start = user_order.total_numbers(user_order)
        total_finish, total_today_finish = user_order.total_numbers(user_order)
        assert total_start == total_finish - 1
        assert total_today_start == total_today_finish - 1

    def test_orders_all_number_changes(self, user_order):
        """Verify changes of total and totalToday numbers in all_orders."""
        user_order.endpoint = user_order.endpoints.orders_all
        response = user_order.send_requests('get', user_order.endpoint,
                                            None, None)
        total_start = response.json()['total']
        total_today_start = response.json()['totalToday']
        user_order.endpoint = user_order.endpoints.orders
        total_finish, total_today_finish = user_order.total_numbers(user_order)
        assert total_start == total_finish - 1
        assert total_today_start == total_today_finish - 1

    @allure.issue("Invalid calculation price for orders with Buns")
    def test_orders_price(self, user_order):
        """Verify price of order with bun."""
        response = user_order.do_order(user_order)
        order_price = response.json()['order']['price']
        price = 0
        for ingredient in response.json()['order']['ingredients']:
            if ingredient['type'] == 'bun':
                price += ingredient['price'] * 2
            else:
                price += ingredient['price']
        assert price == order_price

    @allure.issue("No token validation in post order request")
    @pytest.mark.parametrize('token, exp', invalid_token)
    def test_authorization_validation(self, user_order, token, exp):
        """Verify response code with invalid token."""
        user_order.header = user_order.header_auth(token)
        order = user_order.setup_order(buns=True,
                                       ingr_number=2)
        response = user_order.send_requests('post',
                                            user_order.endpoint,
                                            user_order.header,
                                            order)
        assert response.status_code == exp
        user_order.attach_response(response)
