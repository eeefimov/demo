"""
Class for handling ORDERS api requests.
[FEATURES]:
    Set up a user order with specified ingredients.
    Perform the user order based on specified conditions.
    Get the total numbers of orders and total orders today.
    Check the length of the order ingredients
    with an option to include buns.
"""
from random import choice
import allure
from api.base import BASEAPI


class ORDERS(BASEAPI):
    """Class for handling ORDER api requests."""
    def __init__(self):
        super().__init__()
        self.endpoint = self.endpoints.orders_all
        self.header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.empty_order = {
            "success": False,
            "message": "Ingredient ids must be provided"
        }

    @staticmethod
    @allure.step('Setup User order')
    def setup_order(empty: bool = False,
                    buns: bool = False,
                    buns_number: int = 1,
                    ingr_number: int = 0,
                    ):
        """Set up a user order with specified ingredients."""
        order: list = []
        complete_order = {
            "ingredients": order
        }

        if empty:  # empty order
            with allure.step("Set empty order"):
                return complete_order

        else:
            data = BASEAPI.load_data_from_file('ingredients.json')

            if buns:  # buns in order
                with allure.step("Set buns in order"):
                    for _ in range(0, buns_number):
                        bun_items = [item for item
                                     in data['data']
                                     if item['type'] == 'bun']
                        order.append(choice([item['_id'] for item
                                             in bun_items]))

            if ingr_number > 0:  # number of ingredients in order
                with allure.step("Set ingredients in order"):
                    non_bun_items = [item for item
                                     in data['data']
                                     if item['type'] != 'bun']
                    for _ in range(ingr_number):
                        order.append(choice([item['_id'] for item
                                             in non_bun_items]))

            ORDERS.attach_response(complete_order)
            return complete_order

    @staticmethod
    @allure.step('Send POST request with user oder')
    def do_order(user_order):
        """Perform the user order based on specified conditions."""
        order = user_order.setup_order(buns=True, ingr_number=3)
        response = user_order.send_requests('post',
                                            user_order.endpoint,
                                            user_order.header,
                                            order)
        ORDERS.attach_response(response)
        return response

    @staticmethod
    @allure.step('Get the total number of orders')
    def total_numbers(user_order):
        """Get the total numbers of orders and total orders today."""
        ORDERS.do_order(user_order)
        response = user_order.send_requests('get',
                                            user_order.endpoint,
                                            user_order.header, None)
        assert response.status_code == 200
        return response.json()['total'], response.json()['totalToday']

    @staticmethod
    @allure.step('Check number of ingredients in order')
    def check_len(order: dict, bun: bool) -> int:
        """Check the length of the order ingredients
        with an option to include buns."""
        ln = len(order['order']['ingredients'])
        if bun:
            ln += 1
        return ln
