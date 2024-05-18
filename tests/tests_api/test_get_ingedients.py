"""
[tests AMOUNT]: 7
[tests DEFINITIONS]:
    Get request for /ingredients endpoint.
    Ingredients information.
    (Optional) Post request for /auth/register.
[tests FEATURES]:
    Verify response status code.
    Verify exist of payload in response.
    Verify number of ingredients.
    Verify values of ingredient items.
    Verify response code with invalid methods.
    Verify status code with different type of headers.
"""
import pytest
from data_models.ingredients_models import IngredientsModel, get_data
from params_api.api_ingredients import invalid_methods, header_validation


class TestIngredients:
    """Tests for /ingredients endpoint."""
    def test_status_code(self, ingredients):
        """Verify response status code."""
        response = ingredients.get_request(ingredients.endpoint)
        assert response.status_code == 200

    def test_response_payload(self, ingredients):
        """Verify exist of payload in response."""
        response = ingredients.get_request(ingredients.endpoint)
        assert response.json()

    def test_ingredients_number(self, ingredients):
        """Verify number of ingredients."""
        response = ingredients.get_request(ingredients.endpoint)
        payload = ingredients.load_data_from_file("ingredients.json")
        model = ingredients.get_model(IngredientsModel, response.json())
        assert len(model.data) == len(payload['data'])

    def test_payload_values_validation(self, ingredients):
        """Verify values of ingredient items."""
        response = get_data(ingredients.get_request(
            ingredients.endpoint).json())
        response_model = ingredients.get_model(IngredientsModel, response)
        payload = ingredients.load_data_from_file("ingredients.json")
        payload_model = ingredients.get_model(IngredientsModel, payload)
        assert response_model == payload_model

    @pytest.mark.parametrize('method, exp', invalid_methods)
    def test_invalid_methods(self, ingredients, method, exp):
        """Verify response code with invalid methods."""
        response = ingredients.send_requests(method, ingredients.endpoint,
                                             None, None)
        assert response.status_code == exp
        ingredients.attach_response(response.text)

    @pytest.mark.parametrize('headers, exp', header_validation)
    def test_headers(self, ingredients, register, headers, exp):
        """Verify status code with different type of headers."""
        headers = ingredients.setup_headers(headers, register)
        response = ingredients.send_requests('get', ingredients.endpoint,
                                             headers, None)
        assert response.status_code == exp
