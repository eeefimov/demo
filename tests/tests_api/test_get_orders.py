"""
[tests AMOUNT]: 7
[tests DEFINITIONS]:
    Get request for /orders/all endpoint.
    (Optional) Post request for /auth/register.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify types values in response.
    Verify number of orders.
    Verify response code with invalid methods.
    Verify status code with different headers.
"""
import pytest
from data_models.orders_model import OrdersModel
from params_api.api_ingredients import invalid_methods, header_validation


class TestGetOrdersAll:
    """Class for testing /orders/all endpoint."""
    def test_status_code(self, orders):
        """Verify response status code."""
        response = orders.get_request(orders.endpoint)
        assert response.status_code == 200

    def test_response_payload(self, orders):
        """Verify exist of payload in response."""
        response = orders.get_request(orders.endpoint)
        assert response.json()

    def test_payload_type_validation(self, orders):
        """Verify types values in response."""
        response = orders.get_request(orders.endpoint)
        model = orders.get_model(OrdersModel, response.json())
        assert isinstance(model, OrdersModel)

    def test_orders_number(self, orders):
        """Verify number of orders."""
        response = orders.get_request(orders.endpoint)
        assert len(response.json()['orders']) == 50

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, orders, method, exp):
        """Verify response code with invalid methods."""
        response = orders.send_requests(method, orders.endpoint,
                                        orders.header, None)
        assert response.status_code == exp
        orders.attach_response(response.text)

    @pytest.mark.parametrize('headers, exp', header_validation)
    def test_headers(self, orders, register, headers, exp):
        """Verify status code with different headers."""
        headers = orders.setup_headers(headers, register)
        response = orders.send_requests('get', orders.endpoint,
                                        headers, None)
        assert response.status_code == exp
