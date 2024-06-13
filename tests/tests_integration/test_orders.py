"""
[tests FEATURES]:
    Verify order number changes.
"""
from pages.orders_page_class import ORDERS


def test_orders_number(user_order, orders_page):
    """Verify order number changes."""
    ui_order_number = ORDERS.get_last_order_number(orders_page)
    response = user_order.do_order(user_order)
    assert response.status_code == 200
    api_new_order_number = int(response.json()['order']['number'])
    assert api_new_order_number == ui_order_number + 1
    assert api_new_order_number == ORDERS.get_last_order_number(orders_page)
